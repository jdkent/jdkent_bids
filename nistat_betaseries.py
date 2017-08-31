import os
from nilearn import plotting
from nistats.first_level_model import first_level_models_from_bids

task_label = 'flanker'
space_label = 'MNI152NLin2009cAsym'
data_dir = '/home/james/vosslabhpc/Projects/PACR-AD/Imaging/BIDS'
data_dir2 = '/home/james/Pictures/ds01'
derivatives_folder='derivatives/fmriprep'

models, models_run_imgs, models_events, models_confounds = first_level_models_from_bids(
        data_dir2, task_label, space_label,
        t_r=2.0, slice_time_ref=0.5,
        hrf_model='canonical with derivative',
        signal_scaling=0, verbose=3, n_jobs=-2,
        derivatives_folder=derivatives_folder,
        img_filters=[('variant', 'smoothAROMAnonaggr')])
