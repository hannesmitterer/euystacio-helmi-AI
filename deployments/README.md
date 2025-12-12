# Deployment Records

This directory contains deployment records for smart contracts across different networks.

## Structure

- `sepolia/` - Sepolia testnet deployments
- `polygon/` - Polygon mainnet deployments  
- `hardhat/` - Local Hardhat network deployments

## Format

Each deployment creates a JSON file with the following information:
- Network name
- Environment (staging/production)
- Timestamp
- Deployer address
- Commit hash
- Contract addresses

## Usage

Deployment records are automatically created by the `deploy-contracts.yml` workflow.

Manual deployments should also create records in the same format for tracking.
