from brian2 import *
import numpy as np

from gfs_version_2 import gfs_object


def first_crossing_latency_ms(voltage_mV, time_ms, threshold_mV, stim_onset_ms):
    idx = np.flatnonzero((voltage_mV >= threshold_mV) & (time_ms >= stim_onset_ms))
    if idx.size == 0:
        return np.nan
    return float(time_ms[int(idx[0])] - stim_onset_ms)


def _run_trial_once(
    params=None,
    stim_amp=120 * nA,
    pre_stim=1 * ms,
    stim_duration=0.03 * ms,
    post_stim=8 * ms,
    threshold_mV=-30.0,
    dt=0.01 * ms,
    voltage_limit_mV=1e3,
):
    start_scope()
    defaultclock.dt = dt

    model = gfs_object(params=params)

    mon_gf = StateMonitor(model.GF, 'v', record=[len(model.GF) - 1])
    mon_ttm = StateMonitor(model.TTMn, 'v', record=[len(model.TTMn) - 1])
    mon_psi = StateMonitor(model.PSI, 'v', record=[len(model.PSI) - 1])
    mon_dlm = StateMonitor(model.DLMn, 'v', record=[len(model.DLMn) - 1])
    model.net.add(mon_gf, mon_ttm, mon_psi, mon_dlm)

    model.net.run(pre_stim)
    model.GF.I_inj[0] = stim_amp
    model.net.run(stim_duration)
    model.GF.I_inj[0] = 0 * amp
    model.net.run(post_stim)

    t_ms = np.asarray(mon_ttm.t / ms)
    stim_onset_ms = float(pre_stim / ms)

    gf_v = np.asarray(mon_gf.v[0] / mV)
    ttm_v = np.asarray(mon_ttm.v[0] / mV)
    psi_v = np.asarray(mon_psi.v[0] / mV)
    dlm_v = np.asarray(mon_dlm.v[0] / mV)

    if (
        np.any(~np.isfinite(gf_v))
        or np.any(~np.isfinite(ttm_v))
        or np.any(~np.isfinite(psi_v))
        or np.any(~np.isfinite(dlm_v))
        or np.nanmax(np.abs(gf_v)) > voltage_limit_mV
        or np.nanmax(np.abs(ttm_v)) > voltage_limit_mV
        or np.nanmax(np.abs(psi_v)) > voltage_limit_mV
        or np.nanmax(np.abs(dlm_v)) > voltage_limit_mV
    ):
        raise FloatingPointError('Numerical instability detected (non-finite or exploded voltages).')

    ttm_latency = first_crossing_latency_ms(ttm_v, t_ms, threshold_mV, stim_onset_ms)
    dlm_latency = first_crossing_latency_ms(dlm_v, t_ms, threshold_mV, stim_onset_ms)

    if np.isfinite(ttm_latency):
        ttm_latency += float(model.neuromuscular_junction_delay / ms)
    if np.isfinite(dlm_latency):
        dlm_latency += float(model.neuromuscular_junction_delay / ms)

    return {
        't_ms': t_ms,
        'GF_mV': gf_v,
        'TTMn_mV': ttm_v,
        'PSI_mV': psi_v,
        'DLMn_mV': dlm_v,
        'TTMn_latency_ms': ttm_latency,
        'DLMn_latency_ms': dlm_latency,
    }


def run_trial(
    params=None,
    stim_amp=120 * nA,
    pre_stim=1 * ms,
    stim_duration=0.03 * ms,
    post_stim=8 * ms,
    threshold_mV=-30.0,
    dt_schedule=(0.005 * ms, 0.0025 * ms, 0.001 * ms),
    verbose_retries=False,
):
    last_error = None
    for dt in dt_schedule:
        try:
            return _run_trial_once(
                params=params,
                stim_amp=stim_amp,
                pre_stim=pre_stim,
                stim_duration=stim_duration,
                post_stim=post_stim,
                threshold_mV=threshold_mV,
                dt=dt,
            )
        except Exception as exc:
            last_error = exc
            if verbose_retries:
                print(f'run_trial retry with smaller dt after failure at dt={float(dt/ms):.4f} ms: {exc}', flush=True)

    print(f'run_trial failed for all dt values; returning NaN latencies. Last error: {last_error}', flush=True)
    return {
        't_ms': np.array([], dtype=float),
        'GF_mV': np.array([], dtype=float),
        'TTMn_mV': np.array([], dtype=float),
        'PSI_mV': np.array([], dtype=float),
        'DLMn_mV': np.array([], dtype=float),
        'TTMn_latency_ms': np.nan,
        'DLMn_latency_ms': np.nan,
    }


def sweep_1d(param_name, values, base_params=None, run_kwargs=None):
    base_params = {} if base_params is None else dict(base_params)
    run_kwargs = {} if run_kwargs is None else dict(run_kwargs)
    ttm = np.full(len(values), np.nan)
    dlm = np.full(len(values), np.nan)

    for i, value in enumerate(values):
        params = dict(base_params)
        params[param_name] = value
        result = run_trial(params=params, **run_kwargs)
        ttm[i] = result['TTMn_latency_ms']
        dlm[i] = result['DLMn_latency_ms']

    return ttm, dlm


def sweep_2d(param_y, y_values, param_x, x_values, base_params=None, penalty_ms=5.0, run_kwargs=None):
    base_params = {} if base_params is None else dict(base_params)
    run_kwargs = {} if run_kwargs is None else dict(run_kwargs)
    ttm = np.full((len(y_values), len(x_values)), np.nan)
    dlm = np.full((len(y_values), len(x_values)), np.nan)

    total = len(y_values) * len(x_values)
    done = 0

    for i, yv in enumerate(y_values):
        for j, xv in enumerate(x_values):
            params = dict(base_params)
            params[param_y] = yv
            params[param_x] = xv
            result = run_trial(params=params, **run_kwargs)
            ttm_val = result['TTMn_latency_ms']
            dlm_val = result['DLMn_latency_ms']
            ttm[i, j] = penalty_ms if not np.isfinite(ttm_val) else ttm_val
            dlm[i, j] = penalty_ms if not np.isfinite(dlm_val) else dlm_val

            done += 1
            if done == 1 or done % 20 == 0 or done == total:
                print(
                    f"[{done:4d}/{total:4d}] {param_y}={yv} | {param_x}={xv} "
                    f"-> TTMn={ttm[i, j]:.4f} ms, DLMn={dlm[i, j]:.4f} ms",
                    flush=True,
                )

    return ttm, dlm
