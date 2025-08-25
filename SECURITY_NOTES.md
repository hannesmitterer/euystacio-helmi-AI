# Security Notes & Manual Steps (must read before deployment)

1) **Create Council SSH Keys**  
   - Distribute private keys only to named council members (Alfred, Sara, Bioarchitettura, Dietmar).

2) **Create LUKS Encrypted Vault on the server**  
   Example steps:
dd if=/dev/zero of=/srv/astrod_kernel/astrod_vault.img bs=1M count=200
   cryptsetup luksFormat /srv/astrod_kernel/astrod_vault.img
   cryptsetup open /srv/astrod_kernel/astrod_vault.img astrod_vault
   mkfs.ext4 /dev/mapper/astrod_vault
   mount /dev/mapper/astrod_vault /mnt/astrod_vault
