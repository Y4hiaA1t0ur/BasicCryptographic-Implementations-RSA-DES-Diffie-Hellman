# BasicCryptographic-Implementations-RSA-DES-Diffie-Hellman

This repository contains basic cryptographic implementations of **RSA**, **DES**, and **Diffie-Hellman** algorithms, implemented from scratch in Python for educational purposes. 

**Disclaimer**: These implementations are **not secure** and should **never** be used in production environments. They are intended to demonstrate the basic principles behind these cryptographic algorithms, and their purpose is solely for learning and experimentation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Security Warning](#security-warning)

## Overview

This project includes:
- **RSA**: Public key cryptosystem for encryption and signing messages.
- **DES**: Symmetric key block cipher using Electronic Codebook (ECB) mode.
- **Diffie-Hellman**: Key exchange protocol for securely sharing keys over an insecure channel.

The code implements basic versions of these algorithms and demonstrates how they can be used to exchange and secure messages.

## Features

- **RSA**: 
  - Key generation, encryption, and decryption.
  - Signing and verification of messages using RSA.

- **DES**: 
  - Basic DES encryption and decryption using ECB mode.
  - Can be used to encrypt and decrypt messages using symmetric keys.

- **Diffie-Hellman**: 
  - Secure key exchange between two parties.
  - Used to create a shared secret key over an insecure channel.

## Security Warning

**Do not use this code in any real-world application!**

- **DES**: The DES algorithm is **deprecated** and is **not secure** by modern standards. It uses a 56-bit key, which is vulnerable to brute-force attacks.
- **RSA**: Although RSA is widely used, the implementation here is basic and lacks proper padding, making it vulnerable to various attacks.
- **Diffie-Hellman**: The Diffie-Hellman key exchange is simplified and not intended for real-world cryptographic use.

This project is for educational purposes only and should **not** be used in any production or security-critical system.

