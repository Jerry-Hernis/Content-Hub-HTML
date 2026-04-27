import os
import re

# The pages to include in the SPA and their order
pages = [
    # MAIN FLOW
    "home_contenthub",
    "about_contenthub",
    "pricing_contenthub",
    "login_contenthub",
    "register_contenthub",
    "dashboard_contenthub",
    "agenda_detail_contenthub",
    "kalender_berlabel",
    
    # PRICING FLOW
    "metode_pembayaran",
    "detail_transaksi",
    "konfirmasi_pembayaran",
    
    # CALENDAR FLOW
    "pilih_tanggal",
    "atur_jam",
    "tambahkan_template",
    "preview_template",
    "transisi_ke_canva",
    "drag_drop_konten",
    "menu_edit_jadwal",
    "tambah_label",
    
    # TEMPLATE FLOW
    "templates_contenthub",
    "pencarian_template",
    "hasil_pencarian",
    
    # PROFILE & HELP
    "help_center",
    "profil_pengguna",
    "ganti_akun"
]

base_dir = r"d:\DONLODAN & PROJECT\ContentHub\HTMLCONTENTHUB"

head_content = ""
combined_body = f"""
<!-- SPA Navigation UI / Global Container -->
<div id="spa-app-container">
"""

home_path = os.path.join(base_dir, "home_contenthub", "code.html")
if os.path.exists(home_path):
    with open(home_path, "r", encoding="utf-8") as f:
        home_html = f.read()
        head_match = re.search(r"<head>(.*?)</head>", home_html, re.IGNORECASE | re.DOTALL)
        if head_match:
            head_content = head_match.group(1)

# Extract bodies of all pages
for page in pages:
    page_path = os.path.join(base_dir, page, "code.html")
    if not os.path.exists(page_path):
        page_path = os.path.join(base_dir, page, "index.html")
        if not os.path.exists(page_path):
            print(f"Warning: Could not find HTML file for {page}")
            continue

    with open(page_path, "r", encoding="utf-8") as f:
        html = f.read()
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.IGNORECASE | re.DOTALL)
        if body_match:
            b_content = body_match.group(1)
            # Wrap the content
            display_style = "block" if page == "home_contenthub" else "none"
            combined_body += f'\n<section id="{page}" class="spa-page" style="display: {display_style}; width: 100%; min-height: 100vh;">\n'
            combined_body += b_content
            combined_body += f'\n</section>\n'

combined_body += """
</div>

<!-- SPA Routing Logic -->
<script>
    function navigateTo(pageId) {
        if (!pageId) return;
        
        // Ensure page exists
        const targetPage = document.getElementById(pageId);
        if (!targetPage) {
            console.warn(`Page not found: ${pageId}`);
            return;
        }

        // Hide all pages
        document.querySelectorAll('.spa-page').forEach(page => {
            page.style.display = 'none';
        });
        
        // Show target page
        targetPage.style.display = 'block';
        window.scrollTo(0, 0);
        console.log(`Navigated to ${pageId}`);
    }

    // Search Input Logic (Enter Key)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const targetEl = e.target;
            if (targetEl.tagName.toLowerCase() === 'input') {
                const placeholder = (targetEl.getAttribute('placeholder') || '').toLowerCase();
                if (placeholder.includes('cari') || placeholder.includes('search') || placeholder.includes('template') || placeholder.includes('fashion')) {
                    e.preventDefault();
                    navigateTo('hasil_pencarian');
                }
            }
        }
    });

    // Smart Event Delegation
    document.addEventListener('click', function(e) {
        // Find if clicked element or its parent is an interactive element
        const targetEl = e.target.closest('a, button, [role="button"]');
        
        // Calendar Date Cell click detection
        const calendarCell = e.target.closest('.bg-surface.h-40.p-3');
        const isClickingContent = e.target.closest('.bg-surface-container-lowest.rounded-3xl');
        
        // If clicking on a date cell, but not on an existing content/schedule
        if (calendarCell && !isClickingContent && !targetEl) {
            e.preventDefault();
            navigateTo('atur_jam');
            return;
        }

        // If clicking on an existing schedule in the calendar -> edit jadwal
        if (isClickingContent && !targetEl) {
             e.preventDefault();
             navigateTo('menu_edit_jadwal');
             return;
        }

        // Profile click in Sidebar
        const profileDiv = e.target.closest('img.w-10.h-10.rounded-full');
        // specifically targeting the user profile in sidebar (which might have Rina Wijaya text near it)
        if (profileDiv && profileDiv.closest('aside') && !targetEl) {
             e.preventDefault();
             navigateTo('profil_pengguna');
             return;
        }
        
        // Drag and drop mock (click on a specific draggable looking handle if it exists, or use the drag_drop_konten page for something else)
        // We can route "Geser Tanggal" text to drag_drop_konten
        
        // Calendar icon shortcut in Dashboard
        const calendarIcon = e.target.closest('img[data-alt*="calendar"], img[src*="calendar"]');
        if (calendarIcon && !targetEl) {
             e.preventDefault();
             navigateTo('kalender_berlabel');
             return;
        }

        if (targetEl) {
            const text = (targetEl.innerText || '').trim().toLowerCase();
            const href = targetEl.getAttribute('href');
            let route = null;

            // ---- TEXT / CONTENT BASED MAPPING (USER FLOW) ----
            
            // 1. AUTH FLOW
            if (text.includes('login') || text.includes('log in') || text === 'masuk') route = 'login_contenthub';
            else if (text.includes('register') || text.includes('daftar sekarang') || text.includes('daftar gratis')) route = 'register_contenthub';
            else if (text.includes('masuk ke dashboard') || text.includes('lanjut ke profil bisnis') || text.includes('masuk ke workspace')) route = 'dashboard_contenthub';
            else if (text.includes('mulai gratis')) route = 'login_contenthub';

            // 2. DASHBOARD FLOW
            else if (text.includes("today's agenda") || text.includes('today’s agenda') || text.includes('agenda hari ini')) route = 'agenda_detail_contenthub';
            else if (text.includes('view all library') || text.includes('lihat semua')) route = 'agenda_detail_contenthub';
            else if (text === 'dashboard') route = 'dashboard_contenthub';
            else if (text === 'calendar' || text === 'kalender') route = 'kalender_berlabel';
            else if (text.includes('start create')) route = 'kalender_berlabel'; // CTA Utama

            // 3. CALENDAR CONTENT FLOW
            else if (text.includes('atur jam') || text.includes('ubah jam')) route = 'atur_jam';
            else if (text.includes('simpan waktu') || text.includes('lanjut')) route = 'tambahkan_template';
            else if (text.includes('pilih template unutk jadwal hari ini') || text.includes('pilih template untuk jadwal')) route = 'templates_contenthub';
            else if (text.includes('preview') || text.includes('pilih template')) route = 'preview_template';
            else if (text.includes('gunakan template')) route = 'transisi_ke_canva';
            else if (text.includes('tambahkan ke kalender') || text.includes('tambahkan ke calendar')) route = 'kalender_berlabel';
            else if (text.includes('edit jadwal') || text.includes('edit schedule')) route = 'menu_edit_jadwal';
            else if (text.includes('tambahkan label') || text.includes('tambah label')) route = 'tambah_label';
            else if (targetEl.querySelector('[data-icon="delete"]') || text.includes('hapus')) route = 'kalender_berlabel'; // Hapus -> return to calendar
            else if (text.includes('drag & drop') || text.includes('geser')) route = 'drag_drop_konten';
            
            // 4. PRICING & PAYMENT FLOW
            else if (text === 'pricing' || text.includes('harga')) route = 'pricing_contenthub';
            else if (text.includes('pilih paket pro') || text.includes('pilih paket')) route = 'metode_pembayaran';
            else if (text.includes('pilih & bayar') || text.includes('pilih dan bayar')) route = 'detail_transaksi';
            else if (text.includes('lanjutkan') || text.includes('detail transaksi')) route = 'detail_transaksi';
            else if (text.includes('konfirmasi') || text.includes('lakukan pembayaran')) route = 'konfirmasi_pembayaran';
            else if (text.includes('saya sudah bayar')) route = 'dashboard_contenthub';

            // 5. TEMPLATE FLOW
            else if (text === 'template' || text.includes('jelajahi template')) route = 'templates_contenthub';
            else if (text.includes('cari') || text.includes('search')) route = 'pencarian_template';
            
            // 6. SIDEBAR & PROFILE
            else if (text.includes('help center') || text.includes('bantuan')) route = 'help_center';
            else if (text.includes('ganti akun')) route = 'ganti_akun'; 
            else if (text.includes('profile') || text.includes('edit akun') || text.includes('edit profile')) route = 'profil_pengguna';
            else if (text.includes('logout') || text.includes('keluar')) route = 'home_contenthub';
            
            // Others
            else if (text === 'home') route = 'home_contenthub';
            else if (text === 'about') route = 'about_contenthub';
            else if (text.includes('batal')) route = 'kalender_berlabel'; // Cancel popup

            // ---- HREF BASED FALLBACK ----
            if (!route && href) {
                if (href.includes('login')) route = 'login_contenthub';
                else if (href.includes('register')) route = 'register_contenthub';
                else if (href.includes('dashboard')) route = 'dashboard_contenthub';
                else if (href.includes('calendar')) route = 'kalender_berlabel';
                else if (href.includes('pricing')) route = 'pricing_contenthub';
                else if (href.includes('template')) route = 'templates_contenthub';
                else if (href.includes('metode_pembayaran')) route = 'metode_pembayaran';
                else if (href.includes('_contenthub')) {
                    const parts = href.split('/');
                    const dirName = parts[parts.length - 2];
                    if (document.getElementById(dirName)) {
                        route = dirName;
                    }
                }
            }

            // ---- EXECUTE ROUTE ----
            if (route) {
                e.preventDefault();
                navigateTo(route);
            } else if (href && (href === '#' || href.startsWith('javascript:'))) {
                // Prevent scroll-to-top for unhandled empty links
                e.preventDefault();
            }
        }
    });
</script>
"""

final_html = f"""<!DOCTYPE html>
<html lang="id" class="light">
<head>
{head_content}
    <style>
        /* SPA Transition Styles for Smoothness */
        .spa-page {{
            animation: fadeIn 0.3s ease-in-out;
            position: relative;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Cursor hints for clickable areas in calendar */
        .bg-surface.h-40.p-3 {{
            cursor: pointer;
        }}
        img.w-10.h-10.rounded-full {{
            cursor: pointer;
        }}
    </style>
</head>
<body class="bg-surface text-on-surface selection:bg-primary-fixed m-0 p-0 overflow-x-hidden">
{combined_body}
</body>
</html>
"""

output_path = os.path.join(base_dir, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully built SPA into {output_path}")
