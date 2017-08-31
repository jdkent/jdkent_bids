import os
from nilearn import plotting
from nistats.first_level_model import first_level_models_from_bids
import nibabel as nib

task_label = 'flanker'
space_label = 'MNI152NLin2009cAsym'
data_dir = '/home/james/vosslabhpc/Projects/PACR-AD/Imaging/BIDS'
data_dir2 = '/home/james/Pictures/ds01'
derivatives_folder='derivatives/fmriprep'
# check docs about hrf_model
models, models_run_imgs, models_events, models_confounds = first_level_models_from_bids(
        data_dir2, task_label, space_label,
        t_r=2.0, slice_time_ref=0.5,
        hrf_model='glover + derivative + dispersion',
        signal_scaling=0, verbose=3, n_jobs=-2,
        derivatives_folder=derivatives_folder,
        img_filters=[('variant', 'smoothAROMAnonaggr')])

for sub_idx,sub_model in enumerate(models):
    for run_idx, run_events in enumerate(models_events[sub_idx]):
        run_events_temp = run_events.copy()
        run_events_temp['trial_type'] = 'other_trials'
        for trial in range(len(run_events)):
            run_events_temp.loc[trial, 'trial_type'] = run_events.loc[trial, 'trial_type']
            #fitmodel
            sub_model.fit(models_run_imgs[sub_idx][run_idx],run_events_temp)
            #compute contrast
            img = sub_model.compute_contrast(contrast_def=run_events_temp.loc[trial, 'trial_type'], output_type='effect_size')
            #save img
            nib.save(img, os.path.join(data_dir2,'derivatives/nistats_betaseries/sub-GE140','sub-GE140'+run_events_temp.loc[trial,'trial_type']+str(trial)))
            run_events_temp.loc[trial, 'trial_type'] = 'other_trials'
            #os.mkdir(os.path.join(data_dir2,'derivatives/nistats_betaseries/sub-GE140'))

            #save img


        #sub_models = [ses_model.loc[trial,'trial_type'].replace('other_trials',ses_events.loc[trial, 'trial_type']) for trial in range(len(ses_events))]
