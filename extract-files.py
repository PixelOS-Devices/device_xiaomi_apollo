#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import re

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10098', '0')
        .regex_replace('0x1F', '0x0'),
    'vendor/etc/init/init.batterysecret.rc': blob_fixup()
        .regex_replace('.*seclabel u:r:batterysecret:s0\n', ''),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .add_line_if_missing('LEGACY_MIFARE_READER=1'),
    'vendor/lib/hw/audio.primary.apollon.so': blob_fixup()
        .binary_regex_replace(
            b'/vendor/lib/liba2dpoffload.so',
            b'liba2dpoffload_apollon.so\x00\x00\x00\x00',
        ),
    'vendor/lib64/camera/components/com.mi.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    'vendor/lib64/libril-qc-hal-qmi.so': blob_fixup()
        .regex_replace('ro\.product\.vendor\.device', 'ro\.vendor\.radio\.midevice'),
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .binary_regex_replace(b'\x9A\x0A\x00\x94', b'\x1F\x20\x03\xD5'),
    'vendor/etc/init/init.mi_thermald.rc': blob_fixup()
        .regex_replace(r'seclabel u:r:mi_thermald:s0\n', ''),
    'vendor/etc/init/init_thermal-engine.rc': blob_fixup()
        .regex_replace(r'^#(service\b.*\n(?:    .*\n)*)', r'\1', flags=re.MULTILINE),
    'vendor/lib64/libdlbdsservice.so|vendor/lib/libstagefright_soft_ac4dec.so|vendor/lib/libstagefright_soft_ddpdec.so': blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib64/libarcsoft_single_chart_calibration.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .append('gettid: 1'),
    'vendor/lib64/libwvhidl.so|vendor/lib64/mediadrm/libwvdrmengine.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip

namespace_imports = [
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/qcom-caf/sm8250',
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
]

module = ExtractUtilsModule(
    'apollo',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils(module)
    utils.run()