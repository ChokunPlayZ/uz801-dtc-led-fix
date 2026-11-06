# UZ801 onboard LED correction

Standalone **device-tree fix**, not a userspace LED service. Linux's LED class
and heartbeat trigger provide the behavior without an extra daemon.

Verified on one UZ801 revision: active-high GPIO **71** (status heartbeat),
**73** (WLAN, initially off), **72** (WAN, initially off). The original kernel
profile used GPIO 6/7/8 and did not illuminate that unit's LEDs. Colors have not
been established. The heartbeat indicates Linux activity, **not LTE connectivity**.
Never apply this wiring to the MF800H or an unverified UZ801 revision.

## Build

Needs Python 3 and `dtc` (`brew install dtc`, or Debian's `device-tree-compiler`).
Obtain the **original Linux DTB from your own confirmed board/kernel**, not a
stock Android DTB or another unit's boot image. No device backup is bundled.

```sh
python3 build.py --original /path/to/msm8916-yiming-uz801v3.dtb \
  --output /path/to/NEW-led-build
```

The builder decompiles the original to `original.dts`, applies `stock-leds.dts`
and produces `msm8916-uz801-stock-leds.dtb` in a new output directory. It changes
only LED nodes/pinctrl; the original input is untouched. Existing output paths
are refused. A successful compile does not verify your physical wiring.

## Deployment and recovery

Keep USB SSH and physical boot recovery available. Back up `/boot/extlinux/`
and your original DTB privately. Install the generated DTB under a **new** name
in `/boot/dtbs/qcom/`, deliberately select it in your existing extlinux entry,
review that entry, sync and reboot only when safe. Do not overwrite the original
DTB. No automatic boot editing or reboot script is included because boot
layouts/kernel profiles vary. Restore your saved extlinux configuration to
roll back to the untouched original DTB.

After boot, inspect `/sys/class/leds/uz801:{status,wlan,wan}` and visually confirm
the heartbeat; verify USB, networking and recovery access. Temporary manual
control on the device:

```sh
echo none | sudo tee /sys/class/leds/uz801:status/trigger
echo 1 | sudo tee /sys/class/leds/uz801:status/brightness
echo heartbeat | sudo tee /sys/class/leds/uz801:status/trigger
```

The wiring/heartbeat were historically visually verified and reboot-tested on
one unit. Packaging does not add a new hardware test. See [RELEASE.md](RELEASE.md)
before public distribution.
