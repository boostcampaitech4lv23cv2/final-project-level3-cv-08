# yapf:disable
log_config = dict(
    interval=99,
    hooks=[
        dict(type='TextLoggerHook', by_epoch=False),
        dict(
            type="MMSegWandbHook",
            init_kwargs=dict(
                entity="sawol", project="my-test-project" 
            ),
            num_eval_images=20
            )
    ])
# yapf:enable
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
cudnn_benchmark = True