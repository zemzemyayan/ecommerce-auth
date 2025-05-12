# E-Ticaret Uygulaması Backend Dokümantasyonu

## Proje Tanımı
Bu projede kullanıcı doğrulama, ürün yönetimi ve sepet işlemleri için hibrit bir veri tabanı yapısı kullanılmıştır. Kullanıcılar MySQL veritabanına kayıt olur ve JWT tabanlı bir sistemle giriş yapar. Sepet işlemleri ise MongoDB ile yönetilmektedir.

##  Genel Bakış
MySQL ve MongoDB entegrasyonu ile JWT tabanlı kimlik doğrulama ve rol tabanlı erişim kontrolü sunan e-ticaret backend servisi.

---

##  Temel Özellikler

###  Kimlik Doğrulama
- JWT token tabanlı giriş sistemi
- Token içinde rol bilgisi taşınır (`customer` veya `supplier`)

###  Veritabanı Entegrasyonu
- **MySQL**: Kullanıcı bilgileri (`user_id`, `email`, `password`, `role`)
- **MongoDB**: Sepet ve ürün verileri (referanslı `userId` ile)

###  Rol Tabanlı Sistem
- `customer`: Sepet işlemleri, profil güncelleme
- `supplier`: Ürün ekleme/silme/güncelleme

###  Sepet Yönetimi
- MongoDB'de tutulan sepet verileri
- Soft-delete özelliği ile ürün silme etkisi

---

##  Kullanılan Teknolojiler
| Teknoloji       | Kullanım Amacı               |
|-----------------|-----------------------------|
| MySQL           | Kullanıcı verileri          |
| MongoDB         | Sepet ve ürün verileri      |
| JWT             | Kimlik doğrulama            |
| Bcrypt          | Şifre hashleme              |

---
### API Dokümantasyonu
## Kimlik Doğrulama
# Kayıt Ol
POST /auth/register
Content-Type: application/json

{
  "email": "kullanici@mail.com",
  "password": "Sifre123!",
  "role": "customer"
}
# Giriş Yap
POST /auth/login
Content-Type: application/json

{
  "email": "kullanici@mail.com",
  "password": "Sifre123!"
}
# Şifre Sıfırlama
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "kullanici@mail.com"
}
--> Not: İstek sonucunda terminalde şifre sıfırlama için token gelecektir.
# Yeni Şifre Belirle
POST /auth/reset-password
Content-Type: application/json

{
  "token": "terminalde-gorunen-token",
  "newPassword": "YeniSifre456!"
}
# Profil Güncelleme
PUT /users/profile
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "email": "yeni@mail.com",
  "password": "GuncelSifre789!"
}

## Müşteri İşlemleri
--> Not: Kullanıcı(müşteri) önce giriş yapar ve JWT_TOKEN İLE işlemlerini gerçekleştirir.

# Sepeti Görüntüle
GET /cart
Authorization: Bearer <JWT_TOKEN>

# Sepete Ürün Ekle
POST /cart
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "_id": "mongodb_product_id",
  "quantity": 2
}
# Sepetten Ürün Çıkar
DELETE /cart/:productId
Authorization: Bearer <JWT_TOKEN>

## Tedarikçi İşlemleri (Sadece supplier rolü)
--> Not: Kullanıcı(tedarikçi) önce giriş yapar ve JWT_TOKEN İLE işlemlerini gerçekleştirir.

# Yeni Ürün Ekle
POST /supplier/products
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "product_id": "p001",
  "name": "Laptop",
  "price": 14999.99
}

# Ürün Güncelle
PUT /supplier/products/:id
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "price": 89.99
}

# Ürün Sil (Soft-Delete)
DELETE /supplier/products/:id
Authorization: Bearer <JWT_TOKEN>

# Ürünleri Listeleme
GET http://127.0.0.1:5000/product
Headers:
Authorization: Bearer <token>
Beklenen Yanıt:
[

  {
    "product_id": "p001",
    "name": "Laptop",
    "price": 14999.99
    }
]


### ❗ Önemli Notlar
⚠️ Şifre Sıfırlama:
Şifre sıfırlama linkleri e-posta yerine terminale yazdırılır. Geliştirme ortamında test için bu şekilde tasarlanmıştır.

📌 Profil Bilgileri:
Sistemde sadece email ve password alanları bulunur. Ad/soyad bilgisi tutulmaz.

🚧 Eksik Özellik:
E-posta bildirimleri (Sepetiniz Güncellendi vb.) henüz implemente edilmemiştir.














