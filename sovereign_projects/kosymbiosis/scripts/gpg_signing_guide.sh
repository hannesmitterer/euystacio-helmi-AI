#!/bin/bash

# KOSYMBIOSIS GPG Signing Guide
# Instructions for creating GPG signatures for the archive

cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║              KOSYMBIOSIS GPG Signing Instructions              ║
╚════════════════════════════════════════════════════════════════╝

This guide explains how to create GPG signatures for the KOSYMBIOSIS
archive to ensure authenticity and integrity.

═══════════════════════════════════════════════════════════════
PREREQUISITES
═══════════════════════════════════════════════════════════════

1. GnuPG installed (gpg command available)
2. A GPG key pair generated for your identity
3. Access to the kosymbiosis-archive.zip file

═══════════════════════════════════════════════════════════════
STEP 1: Generate or Import Your GPG Key
═══════════════════════════════════════════════════════════════

If you don't have a GPG key yet:

  gpg --full-generate-key

Follow the prompts:
- Select RSA and RSA (default)
- Key size: 4096 bits (recommended)
- Expiration: Your preference (0 = never expires)
- Enter your name and email
- Set a strong passphrase

If you already have a key, skip to Step 2.

═══════════════════════════════════════════════════════════════
STEP 2: List Your GPG Keys
═══════════════════════════════════════════════════════════════

To see your available keys:

  gpg --list-secret-keys --keyid-format LONG

Example output:
  sec   rsa4096/ABCD1234EFGH5678 2026-01-07 [SC]
        1234567890ABCDEF1234567890ABCDEF12345678
  uid                 [ultimate] Your Name <your.email@example.com>

Note the key ID (e.g., ABCD1234EFGH5678)

═══════════════════════════════════════════════════════════════
STEP 3: Create Your Signature
═══════════════════════════════════════════════════════════════

For the primary creator:

  cd sovereign_projects/kosymbiosis
  gpg --detach-sign --armor -o kosymbiosis.sig kosymbiosis-archive.zip

For co-creator 1:

  gpg --detach-sign --armor -o kosymbiosis-co1.sig kosymbiosis-archive.zip

For co-creator 2:

  gpg --detach-sign --armor -o kosymbiosis-co2.sig kosymbiosis-archive.zip

You'll be prompted for your GPG key passphrase.

═══════════════════════════════════════════════════════════════
STEP 4: Verify Your Signature
═══════════════════════════════════════════════════════════════

Test your signature:

  gpg --verify kosymbiosis.sig kosymbiosis-archive.zip

Expected output:
  gpg: Signature made [date]
  gpg:                using RSA key [key-id]
  gpg: Good signature from "Your Name <your.email@example.com>"

═══════════════════════════════════════════════════════════════
STEP 5: Export Your Public Key
═══════════════════════════════════════════════════════════════

Others need your public key to verify your signature:

  gpg --armor --export your.email@example.com > your-public-key.asc

Share this public key file with the project repository.

═══════════════════════════════════════════════════════════════
STEP 6: Import Other Co-Creators' Public Keys
═══════════════════════════════════════════════════════════════

To verify other signatures, import their public keys:

  gpg --import co-creator-public-key.asc

═══════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════

Problem: "gpg: signing failed: No secret key"
Solution: Make sure you have a secret key. Run gpg --list-secret-keys

Problem: "gpg: signing failed: Inappropriate ioctl for device"
Solution: Run: export GPG_TTY=$(tty)

Problem: Signature verification shows "Can't check signature: No public key"
Solution: Import the signer's public key with gpg --import

═══════════════════════════════════════════════════════════════
BEST PRACTICES
═══════════════════════════════════════════════════════════════

1. Use strong passphrases for GPG keys
2. Keep your private key secure and backed up
3. Consider key expiration dates for enhanced security
4. Publish your public key to key servers:
   gpg --send-keys [your-key-id]
5. Verify the archive checksum before signing

═══════════════════════════════════════════════════════════════
VERIFICATION WORKFLOW
═══════════════════════════════════════════════════════════════

Once all signatures are collected:

1. Ensure all three .sig files are present
2. Run the verification script:
   ./scripts/verify_signatures.sh
3. Confirm all three signatures are valid
4. Proceed with distribution

╔════════════════════════════════════════════════════════════════╗
║                    End of Signing Guide                        ║
╚════════════════════════════════════════════════════════════════╝

For questions or issues, contact:
- Project Lead: hannes.mitterer@gmail.com
- Documentation: sovereign_projects/kosymbiosis/README.md

EOF
