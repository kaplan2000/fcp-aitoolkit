# FCP AI-Toolkit 1.1.1 çıktı: 1.1 artı iki düzeltme

Date: 2026-10-02
Status: Yayımlandı
Language: tr
Canonical: https://www.fcp-aitoolkit.com/tr/blog/fcp-ai-toolkit-1-1-1/

1.1.1; Smart Cache, altyazı düzenleme, Smart Search ve yaklaşık 100 dille Mac App Store’da. Fazladan “.1”, tam zamanında düzelttiğimiz iki hata için.

FCP AI-Toolkit 1.1.1, 30 Eylül’den beri Mac App Store’da. 1.0 sürümünü kullanıyorsanız güncelleme sizin için. Mac App Store’u açın ve her zamanki gibi güncelleyin.


Bu sürüm tek bir şey için: bir kurguya baştan başlamadan geri dönmek. Başka bir stil denersiniz, girişi kısaltırsınız, bir adı düzeltirsiniz, bir klibi uzatırsınız. Altyazılar, her seferinde sıfırdan başlamak yerine sizinle birlikte ilerler.



## Bir dakika, 1.1’e ne oldu?

Yerinde bir soru. 22 Eylül’de bir ön bakış yazısı yayımlamıştık: [1.1 ile geliyor](/tr/blog/fcp-ai-toolkit-1-1-preview/). 1.1 sürümü tamamlanmış ve kontrol edilmişti. Yalnızca lansman videosunu bekliyordu.


Sonra 25 Eylül’de, gerçek Final Cut Pro projelerinde son bir test turu daha yaptık. Birkaç klip, ayrılmış ses; gerçek bir kurgunun getirdiği türden dağınıklık. İki hata çıktı. İkisini de aynı gün düzelttik.


1.1’i yayımlayıp sonradan yama çıkarabilirdik. Önce sürümü düzeltmeyi ve ona yeni bir numara vermeyi tercih ettik. Yani 1.1.1, yalnızca 1.1 artı iki düzeltmedir. Özellikler ön bakışta anlattıklarımızın aynısı; fazladan “.1” ise sizinle buluşmadan önce yakaladığımız iki hatayı temsil ediyor.


1.1.1’i 27 Eylül’de Apple’a gönderdik, 30 Eylül’de yayına girdi. Kimse bir sürümü kaçırmadı: herkese açık bir 1.1 hiç olmadı. 1.0 kullanıyorsanız doğrudan 1.1.1’e geçersiniz.


- 21 Haziran 20261.0 sürümü yayımlandı22 Eylül 20261.1 tanıtıldı, lansman videosunu bekliyor25 Eylül 2026Son test iki hata buldu; ikisi de aynı gün düzeldi
- 27 Eylül 20261.1.1 inceleme için Apple’a gönderildi30 Eylül 20261.1.1 Mac App Store’da yayında

## İlk düzeltme: üst üste binen altyazılar

Analyze düğmesine bastığınızda eklenti, zaman çizelgenizdeki her diyalog klibini ayrı ayrı metne dönüştürür, sonra sonuçları birleştirir. Bazı projelerde bu, aynı satırın iki kez çıkmasına ya da altyazıların üst üste binmesine yol açabiliyordu. Bunun üç yolunu bulduk:




- Kırpılmış bir klip. Zaman çizelgesinde bir klibin başını kestiniz, ama gizli kalan, kırpılmış bölümdeki konuşma yine de altyazı olarak gelebiliyordu.

- Aynı konuşmayı taşıyan iki klip. Kamera sesi ile ayrı bir mikrofonu düşünün; ikisi de diyalog olarak işaretli. Aynı sözler iki kez çıkabiliyordu.

- Konuşma modelinin kendisi. Whisper bazen birbiriyle biraz örtüşen satırlar döndürür.

Tek başına bu sinir bozucu. Ama 1.1.1 bir altyazı editörü de getiriyor ve editör mantıklı bir şey yapıyor: bir altyazının komşusuyla çakışmasına yol açacak her zamanlama değişikliğini reddediyor. Kopyalar zaten çakışırken, denediğiniz her düzeltme reddedilirdi. Kilitlenmiş gibi hissettiren bir editörle çaresiz kalırdınız.


Şimdi olan şu:




- Her klibin altyazıları, kelimeleri ortadan bölmeden, klibin zaman çizelgesinde gerçekten gördüğünüz bölümüne göre kesilir.

- Yinelenen konuşma tek bir altyazıda birleştirilir.

- Geriye kalan her çakışma düzgünce ayrılır.

- Düzeltmeden önce kaydedilen altyazılar yüklenirken otomatik olarak onarılır.

Ayrıca her altyazıda yeni bir kaldırma düğmesi var. İstemediğiniz bir satır varsa silin. Bir sonraki sefer de silinmiş kalır.



## İkinci düzeltme: sandığımız yerde olmayan ses

Bu, videosundan ayrılmış ya da bağlı bir klipte duran sesle ilgili. Sık görülen örnek, ayrı bir kayıt cihazından gelen ve ana klibinize eklenen ses.


Bu projelerde eklenti, zaman çizelgenizdeki konumları yanlış okuyabiliyordu. Test projelerimizden birinde ayrılmış ses, videosundan uzundu. Yalnızca videonun uzunluğu metne dönüştürüldü ve iki kaynak birbirinden 1,6 saniye uzaktaydı. Altyazılar senkrondan çıktı.


Artık iç içe ve bağlı kliplerin konumları doğru hesaplanıyor. Bağlı bir klip, bağlı olduğu klibin uzunluğuna kesilmek yerine kendi hikâye akışı üzerinde ölçülür. Bir video klibin görüntüsü artık ses kaynağı sanılmıyor. Ses rolleri, devre dışı klipler ve kapatılmış ses kanalları da dikkate alınıyor.


İki düzeltme de aynı yerden geldi: gerçek projelerden. Bir kez daha onlarla test ettiğimiz için memnunuz.



## Smart Cache: baştan başlamayın

Smart Cache, Mac’inizde nelerin metne dönüştürüldüğünü hatırlar.


Şöyle düşünün. Bir röportaja altyazı ekliyorsunuz ve sonuçtan memnunsunuz. Sonra müşteri sonuna on saniye daha istiyor. Klibi zaman çizelgesinde uzatıp yeniden Analyze’a basıyorsunuz. Whisper’dan yalnızca yeni, henüz metne dönüştürülmemiş bölüm geçiyor. Gerisi zaten hazır.


Aynı klibi aynı dil ve aynı modelle yeniden çalıştırın; altyazılar anında geri gelir. Kurgu hâlâ değişirken bu işinize yarar: başka bir stil deneyin, yeniden çalıştırın, kısaltın, uzatın; altyazı geçişine sıfırdan başlamadan.


Smart Cache varsayılan olarak açıktır. Kapatmak isterseniz eklentide bir anahtar var. Bir klibin ilk çalıştırması yine ne kadar sürecekse o kadar sürer; bu da Mac’inize, klibinize ve modele bağlıdır. Smart Cache ilk çalıştırmaya değil, ikinci çalıştırmaya yardımcı olur.



## Bir altyazıyı zaman çizelgesine ulaşmadan düzeltin

İyi bir konuşma modeli bile konuğunuzun adını kendi bildiği gibi yazabilir. Artık başlıklar zaman çizelgesine inmeden önce bir adı, bir noktalama işaretini ya da bütün bir ifadeyi doğrudan eklentinin içinde düzeltebilirsiniz.


Her altyazının başlangıç ve bitiş zamanını da değiştirebilirsiniz. Editör, siz ilerledikçe zamanlamanızı denetler. Geçersiz bir aralığı ve komşusuyla çakışan bir altyazıyı reddeder; böylece küçük bir değişiklik diziyi sessizce bozamaz.


Düzenlemeleriniz Mac’inizde kaydedilir. Eklentiyi yeniden açtığınızda ya da aynı medyayı yeniden analiz ettiğinizde geri gelirler. Ayrıca 1.1.1 ile birlikte, istemediğiniz bir altyazıyı kaldırabilirsiniz.



## Smart Search: bunu nerede söylemiştim?

Bir mercekle ilgili bir şey söylediğinizi hatırlıyorsunuz ama hangi videoda olduğunu hatırlamıyorsunuz. Smart Search, tüm kliplerinizde ürettiğiniz her altyazıya bakar. Her sonuçta eşleşen metin, dosya adı ve zaman kodu görünür.


Arama düzeltmelerinizi de görür. Bir adı düzelttiyseniz, bulabileceğiniz ad düzeltilmiş olandır.


Dürüst bir sınır: bir sonuca tıklamak sizi Final Cut Pro’daki klibe götürmez. Dosya adını ve zaman kodunu alırsınız, oraya kendiniz gidersiniz.



## Yaklaşık 100 dil ve Auto Detect

1.0 sürümünde 20 dillik bir seçici vardı. Dil menüsü artık Whisper model kataloğundaki yaklaşık 100 dilin tamamını listeliyor. En üstte yeni bir seçenek var: Auto Detect. Bir klipte hangi dilin konuşulduğundan emin değilseniz ya da kliplerde diller karışıksa, kararı ona bırakın. Auto Detect de model indirildikten sonra Mac’inizde çalışır.


Lütfen bu bölümü dikkatle okuyun. Bu sayı, modelin dil kapsamıdır. Altyazı kalitesini her dilde ayrı ayrı test etmedik. Altyazıların ne kadar doğru olduğu dile, kayda, konuşmacıya ve modele bağlıdır. Bu yüzden altyazılarınızı gözden geçirmek, her dilde işin bir parçası olmaya devam eder. Yeni editörle bu iş daha da hızlı.



## Daha küçük pencereler

Eklenti artık daha küçük Final Cut Pro pencerelerine, örneğin bir dizüstü ekranına uyuyor. Proje bırakma alanı, arama ve şablon seçenekleri erişilebilir kalıyor.



## Aynı kalanlar



- Transkripsiyon hâlâ Mac’inizde çalışır. OpenAI’ın Whisper’ı üzerine kurulu WhisperKit’i kullanıyoruz. Görüntüleriniz bulut tabanlı bir transkripsiyon hizmetine yüklenmez. Konuşma modeli bir kez indirilir ve bunun için internet gerekir. App Store satın almaları ve abonelik kontrolleri de interneti kullanır.

- Aynı beş şablon. Basic, Highlighted, Highlighted with Background, Pop ve Beast Pop. Yazı tipi, renk ve konum hâlâ ayarlanabilir.

- Aynı düzenli sonuç. Başlıklarınız, ikincil bir hikâye akışında tek bir bileşik klipte gruplanmış olarak geri gelir.

- Aynı fiyatlandırma modeli. Uygulamayı indirmek ücretsiz, şablonlar da ücretsiz. Otomatik yapay zekâ altyazıları aktif bir aylık abonelik gerektirir. Güncel fiyatlar için lütfen şuraya göz atın: [Mac App Store sayfası](https://apps.apple.com/app/id6775619373).


## Bu güncellemede olmayanlar

Merak etmenize gerek kalmasın: 1.1.1’de SRT veya başka bir altyazı dosyası dışa aktarımı, metinden konuşma üretimi ve otomatik YouTube yüklemesi yok. Arama kelimeleri bulur, görüntüleri ya da fikirleri değil; yani görsel veya anlamsal arama yok. Ve yukarıda söylediğimiz gibi, bir arama sonucu sizi klibe götürmez.


Bir sonraki güncelleme üzerinde şimdiden çalışıyoruz. Burada bununla ilgili hiçbir söz vermeyeceğiz. Hazır olduğunda size haber vermeyi tercih ederiz.



## Edinin, izleyin, ne düşündüğünüzü söyleyin

Güncellemek için [Mac App Store](https://apps.apple.com/app/id6775619373) uygulamasını açın ve FCP AI-Toolkit 1.1.1’i yükleyin. App Store sayfası artık 10 dilde ve kısa bir önizleme videosu var.


Çalışırken görmek için [YouTube’daki lansman videosunu](https://www.youtube.com/watch?v=ZvGX2RwCvH8)izleyin. İlk videolarımız, yani bir lansman videosu ve Shorts videoları, şu platformlarda yayında: [YouTube](https://www.youtube.com/@FCPAIToolkit) ve [Instagram](https://www.instagram.com/fcpaitoolkit/) (Reels olarak). Ayrıca bizi şurada da bulabilirsiniz: [TikTok](https://www.tiktok.com/@fcpaitoolkit). Buraya nasıl geldiğimizi okumak isterseniz, [1.0 yazısı](/tr/blog/fcp-ai-toolkit-1-0/) ve [1.1 ön bakışı](/tr/blog/fcp-ai-toolkit-1-1-preview/) hâlâ yayında.


Projenizde bir şey çalışmazsa ya da bir fikriniz varsa bize help@fcp-aitoolkit.com adresinden yazın. Gerçek bir sorunu olan gerçek bir proje, alabileceğimiz en iyi testtir. Bu iki hatayı da böyle bulduk.


FCP AI-Toolkit’i kullandığınız için teşekkürler.
