#!/usr/bin/env node
require('dotenv').config();
const { ethers } = require('hardhat');
const { NFTStorage, Blob } = require('nft.storage');
const fs = require('fs');
const Base64 = require('js-base64').Base64;

(async () => {
  try {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying with account:", deployer.address);

    const nftStorage = new NFTStorage({ token: process.env.NFT_STORAGE_KEY });

    // Upload dei file
    const manifestCID = await nftStorage.storeBlob(new Blob([fs.readFileSync('manifest.txt')]));
    const signatureCID = await nftStorage.storeBlob(new Blob([fs.readFileSync('signature.txt')]));
    console.log("Manifest CID:", manifestCID);
    console.log("Signature CID:", signatureCID);

    // Deploy del contratto
    const Manifest = await ethers.getContractFactory("EuystacioManifest");
    const contract = await Manifest.deploy(manifestCID, signatureCID);
    await contract.deployed();
    console.log("EuystacioManifest deployed to:", contract.address);

    // Recupera e decodifica tokenURI
    const tokenURI = await contract.tokenURI(1);
    console.log("Base64 tokenURI:", tokenURI);
    const json = Base64.decode(tokenURI.replace("data:application/json;base64,", ""));
    console.log("Decoded JSON metadata:", json);

  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();
