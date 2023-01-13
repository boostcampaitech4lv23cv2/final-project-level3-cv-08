_base_ = [
    './models/upernet_convnext.py', './datasets/ade20k.py',
    './default_runtime.py', './schedules/schedule_160k.py'
]
crop_size = (512, 512)
model = dict(
    decode_head=dict(in_channels=[128, 256, 512, 1024], num_classes=2),
    auxiliary_head=dict(in_channels=512, num_classes=2),
    test_cfg=dict(mode='slide', crop_size=crop_size, stride=(341, 341)),
)

optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys={
            'pos_block': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.),
            'head': dict(lr_mult=10.)
        }))

lr_config = dict(
    _delete_=True,
    policy='CosineRestart',
    warmup='linear',
    warmup_iters=1000,
    warmup_ratio=1e-6,
    min_lr_ratio=1e-6,
    periods=[20000, 40000, 60000, 80000],
    restart_weights=[1.0, 0.6, 0.4, 0.2],
    by_epoch=False)

# fp16 settings
optimizer_config = dict(type='Fp16OptimizerHook', loss_scale='dynamic')
# fp16 placeholder
fp16 = dict()
