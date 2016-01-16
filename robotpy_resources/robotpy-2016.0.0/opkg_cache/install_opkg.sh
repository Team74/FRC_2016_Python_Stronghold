
set -e
if ! opkg list-installed | grep -F 'python3 - 3.5.1'; then
    opkg install  opkg_cache/python3_3.5.1_cortexa9-vfpv3.ipk
else
    echo "python3 already installed, continuing..."
fi