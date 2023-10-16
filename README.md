![](https://i.ibb.co/sKgtgvc/Screenshot-2023-09-13-at-4-27-40-AM.png)

# Sallt
Virtualized XRP Wallet

**Description**:  Sallt is an open-source XRP (XRP Ledger) software wallet. The main goal of Sallt is to provide enhanced security while maintaining lightweight. Sallt improves on traditional software wallets by introducing *virtualized signing, external private key storage, and end-to-end encryption* that allows for a much more secure experience. As with any software wallet, the security of the host machine remains a responsibility of the end user.



**How It Works**: Sallt attempts to close the gap between hardware and software wallets through its advanced signing mechanism.

‎
*Sallt is currently in its early developmental stages while  virtualized signing remains merely as a Proof-of-Concept*

# Transaction Signing
There are different/traditional ways of signing transactions locally and in a distributed manner. Each have specific pros and cons. Sallt wallet aims to provide a lightweight, but also more secure signing mechanism than other traditional software wallets. However, by following safe practice, if the security of the host/signing machine is compromised then your wallet should be assumed compromised as well.

**Desktop/Software Wallet**

![](https://i.ibb.co/LNtTmxs/normal-signing.jpg)

- Lightweight
- Private keys stored locally (on disk)
- Easy to download, setup, and use

**Web Wallet**

![](https://i.ibb.co/WxB5MBP/web-signing.jpg)

- Extremely lightweight
- Private keys storage and responsibility placed onto provider
- Prone to attacks/security breaches
- Lowest cost of entry, make an account and send payments

**Hardware Wallet**

![](https://i.ibb.co/vHkz7s0/hardware-signing.jpg)

- Generally lightweight enough
- Typically known as the "most secure" production wallet(s)
- High cost of entry, must pay upfront for the hardware solution

**Sallt**

![](https://i.ibb.co/ggf7pgx/sallt-infra.jpg)

- Less Lightweight than a traditional software wallet
- Security lies inbetween a hardware and software wallet (gain security at the expensive of bulkiness)
- Low cost of entry (free), setup streamlined

*Sallt attempts to utilize an air-gapped virtual machine for signing operations, giving you the best of both worlds in terms of ease-of-accessibility of Desktop/Software wallets and security of Hardware wallets.*
