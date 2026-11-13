"""Simulasi Jatuh Bebas dan Pantulan Bola — adaptasi web Kualitas Bagys.py."""

import asyncio
import math
import pygame

pygame.init()
LEBAR, TINGGI = 1000, 680
FPS = 60
SKALA = 65
TANAH_Y = 555
RADIUS = 23
TINGGI_AWAL = 6.0
GRAVITASI_AWAL = 9.81
RESTITUSI_AWAL = 0.78
AMBANG_BERHENTI = 0.45
JUDUL = "Simulasi Jatuh Bebas dan Pantulan Bola"

layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption(JUDUL)
jam = pygame.time.Clock()
# Font bawaan Pygame tersedia juga ketika Arial tidak ada di browser.
font_judul = pygame.font.Font(None, 36)
font_judul.set_bold(True)
font_biasa = pygame.font.Font(None, 28)
font_kecil = pygame.font.Font(None, 24)
PUTIH = (245, 248, 255)
BIRU = (38, 111, 226)
GELAP = (31, 47, 75)
ABU = (107, 123, 148)
HIJAU = (67, 165, 111)


def teks(tulisan, font, warna, x, y):
    layar.blit(font.render(tulisan, True, warna), (x, y))


def reset_simulasi():
    return TINGGI_AWAL, 0.0, 0, 0.0, False


def gambar_latar():
    layar.fill((237, 246, 255))
    for meter in range(8):
        y = int(TANAH_Y - RADIUS - meter * SKALA)
        if 95 < y < TANAH_Y:
            pygame.draw.line(layar, (214, 226, 241), (65, y), (940, y), 1)
            teks(f"{meter} m", font_kecil, ABU, 14, y - 10)
    pygame.draw.rect(layar, (193, 229, 207), (0, TANAH_Y, LEBAR, TINGGI - TANAH_Y))
    pygame.draw.line(layar, HIJAU, (0, TANAH_Y), (LEBAR, TANAH_Y), 5)


def gambar_bola(y_bola, tinggi_meter):
    lebar_bayangan = max(16, int(44 - tinggi_meter * 3))
    pygame.draw.ellipse(layar, (145, 194, 165),
                        (500 - lebar_bayangan, TANAH_Y - 10, 2 * lebar_bayangan, 11))
    pusat = (500, int(y_bola))
    pygame.draw.circle(layar, (24, 82, 167), pusat, RADIUS + 2)
    pygame.draw.circle(layar, BIRU, pusat, RADIUS)
    pygame.draw.circle(layar, (108, 177, 250), (pusat[0] - 8, pusat[1] - 9), 7)


async def main():
    tinggi, kecepatan, pantulan, waktu, jeda = reset_simulasi()
    gravitasi = GRAVITASI_AWAL
    restitusi = RESTITUSI_AWAL
    berjalan = True

    while berjalan:
        dt = min(jam.tick(FPS) / 1000.0, 0.033)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                berjalan = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    berjalan = False
                elif event.key == pygame.K_SPACE:
                    jeda = not jeda
                elif event.key == pygame.K_r:
                    tinggi, kecepatan, pantulan, waktu, jeda = reset_simulasi()
                elif event.key == pygame.K_UP:
                    gravitasi = min(25.0, gravitasi + 0.5)
                elif event.key == pygame.K_DOWN:
                    gravitasi = max(0.5, gravitasi - 0.5)
                elif event.key == pygame.K_RIGHT:
                    restitusi = min(1.0, round(restitusi + 0.05, 2))
                elif event.key == pygame.K_LEFT:
                    restitusi = max(0.0, round(restitusi - 0.05, 2))

        if not berjalan:
            break

        if not jeda and (tinggi > 0 or kecepatan != 0):
            waktu += dt
            tinggi_baru = tinggi - kecepatan * dt - 0.5 * gravitasi * dt**2
            kecepatan_baru = kecepatan + gravitasi * dt
            if tinggi_baru <= 0:
                kecepatan_tumbukan = math.sqrt(max(0.0, kecepatan**2 + 2 * gravitasi * tinggi))
                tinggi = 0.0
                if kecepatan_tumbukan * restitusi > AMBANG_BERHENTI:
                    kecepatan = -restitusi * kecepatan_tumbukan
                    pantulan += 1
                else:
                    kecepatan = 0.0
            else:
                tinggi = tinggi_baru
                kecepatan = kecepatan_baru

        gambar_latar()
        gambar_bola(TANAH_Y - RADIUS - tinggi * SKALA, tinggi)
        teks(JUDUL.upper(), font_judul, GELAP, 70, 22)
        teks("Amati gerak bola, ubah gravitasi dan koefisien restitusi", font_kecil, ABU, 72, 65)
        teks(f"Waktu       : {waktu:6.2f} s", font_biasa, GELAP, 650, 120)
        teks(f"Ketinggian  : {tinggi:6.2f} m", font_biasa, GELAP, 650, 151)
        teks(f"Kecepatan   : {kecepatan:6.2f} m/s", font_biasa, GELAP, 650, 182)
        teks(f"Pantulan    : {pantulan}", font_biasa, GELAP, 650, 213)
        teks(f"Gravitasi   : {gravitasi:.2f} m/s2", font_biasa, GELAP, 650, 244)
        teks(f"Restitusi   : {restitusi:.2f}", font_biasa, GELAP, 650, 275)
        if jeda:
            teks("DIJEDA", font_judul, (201, 103, 35), 422, 300)
        elif tinggi == 0 and kecepatan == 0:
            teks("BOLA BERHENTI", font_biasa, GELAP, 408, 466)
        teks("SPACE: jeda/lanjut    R: ulang    ESC: keluar", font_kecil, GELAP, 55, 590)
        teks("ATAS/BAWAH: gravitasi    KIRI/KANAN: restitusi", font_kecil, GELAP, 55, 644)
        pygame.display.flip()
        # Wajib: beri browser kesempatan memperbarui tampilan dan input.
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
