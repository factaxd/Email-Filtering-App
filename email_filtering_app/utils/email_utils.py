import imaplib
import email
from email.header import decode_header

def decode_mime_words(s):
    decoded_words = decode_header(s)
    decoded_string = ''
    for word, encoding in decoded_words:
        if isinstance(word, bytes):
            try:
                encoding = encoding if encoding else 'utf-8'
                word = word.decode(encoding)
            except LookupError:
                word = word.decode('utf-8', errors='ignore')
        decoded_string += word
    return decoded_string

def fetch_and_process_emails(user, password, keywords, mongo):
    # IMAP sunucusuna bağlan
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(user, password)
    except imaplib.IMAP4.error as e:
        print("Giriş hatası:", e)
        return "Giriş hatası: " + str(e)

    # Posta kutusunu seç (INBOX)
    mail.select("inbox")

    # Tüm e-postaları ara
    status, messages = mail.search(None, "ALL")
    if status != 'OK':
        print("E-posta arama hatası:", status)
        return "E-posta arama hatası: " + str(status)

    # E-posta numaralarını al
    mail_ids = messages[0].split()
    print(f"Toplam {len(mail_ids)} e-posta bulundu.")

    # Her bir e-posta için işlemleri gerçekleştir
    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        if status != 'OK':
            print(f"E-posta {mail_id} alınamadı:", status)
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_mime_words(msg["Subject"])
                sender = msg.get("From")

                # E-posta içeriğini al
                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                            body += part.get_payload(decode=True).decode(errors='ignore')
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')

                # Anahtar kelimelere göre etiketle ve MongoDB'ye kaydet
                for keyword in keywords:
                    if keyword in body:
                        collection = mongo.db[keyword.strip()]
                        collection.insert_one({
                            "sender": sender,
                            "subject": subject,
                            "body": body
                        })
                        print(f"E-posta {mail_id} '{keyword}' olarak etiketlendi.")
                        break  # Anahtar kelime bulunduğunda, diğer anahtar kelimeleri kontrol etmeye gerek yok

    # Oturumu kapat
    mail.logout()
    return "İşlem tamamlandı"
