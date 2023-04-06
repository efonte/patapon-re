# Patapon 3 Encryptor and Decryptor

```bash
patapon3-enc.exe --help
Patapon 3 Encryptor/Decryptor 0.1
efonte
Encrypts or decrypts Patapon 3 files using Camellia cipher

USAGE:
    patapon3-enc.exe [OPTIONS] <input> <output>

ARGS:
    <input>     Sets the input file to use
    <output>    Sets the output file to use

OPTIONS:
    -d, --decrypt     Decrypt the input file instead of encrypting it
    -h, --help        Print help information
    -p, --progress    Show progress bar
    -V, --version     Print version information
```

## Decrypt file

```bash
patapon3-enc.exe DATAMS.BND DATAMS.BND.dec -d -p
```

## Encrypt file

```bash
patapon3-enc.exe DATAMS.BND.dec DATAMS.BND.enc -p
```
