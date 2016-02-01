# Do something to get the data from the pkcs7 wrapper
b = BIO.openfile('test.csr')
p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(b._ptr()), 1)
s = SMIME.SMIME()
sk = X509.X509_Stack()
s.set_x509_stack(sk)
st = X509.X509_Store()
s.set_x509_store(st)
data = s.verify(p7, None, SMIME.PKCS7_NOVERIFY)


# Decrypt the data
b = BIO.MemoryBuffer(pkcs-data-from-above)
p7 = SMIME.PKCS7(m2.pkcs7_read_bio_der(b._ptr()), 1)
k = BIO.MemoryBuffer(cakey)
c = BIO.MemoryBuffer(cacrt)
sender = SMIME.SMIME()
sender.load_key_bio(k, c)
data = sender.decrypt(p7)

data == CSR to sign



-----

CSR in PEM format:
openssl crl2pkcs7 -nocrl -certfile client.pem -outform DER -out client-deg.der

Now we have the degenerate PKCS7. We need to encrypt it with the
original request certificate. Cipher is des-ede3-cbc (des3).
openssl smime -encrypt -in client-deg.der -des3 -binary -outform DER request.crt >client-enc.der

Finally, we need to pkcs7 sign the data with our CA cert & key.
openssl smime -sign -in client-enc.der -signer ca.crt -inkey ca.key -outform DER -nodetach >client.p7

Verify:
openssl smime -verify -in client.p7 -inform DER -CAfile ca.crt

Send client.p7 back with Content-Type: application/x-pki-message


https://github.com/nolanbrown/ios-cert-enrollment/blob/master/lib/ios-cert-enrollment/sign.rb

