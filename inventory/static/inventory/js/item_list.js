document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addItemForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const endpointUrl = form.dataset.addUrl || form.action;

        /* =========================================================================
         * BUG PENJELASAN UNTUK MAHASISWA:
         * 
         * Kode JavaScript di bawah mengirim `formData` langsung via AJAX tanpa
         * mengecek validasi input di client-side.
         * 
         * Jika ada field yang kosong, server Django mengembalikan HTTP 400 (Bad Request)
         * berisi JSON: `{"status": "error", "errors": {"name": ["This field is required."]}}`.
         * 
         * Fungsi `.then(response => response.json())` berikut mengasumsikan respon selalu 200 OK.
         * Saat HTTP 400 diterima, `data` berisi objek error (BUKAN data barang baru).
         * 
         * Akibatnya, `data.name`, `data.price`, dan `data.description` bernilai `undefined`,
         * dan baris `undefined - Rp undefined` tetap ditambahkan ke tabel UI!
         * =========================================================================
         */

        // KODE BUGGY (Belum menangani HTTP 400 & Form Errors):
        fetch(endpointUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            // BUG: Tidak ada pengecekan if (!response.ok)
            return response.json();
        })
        .then(data => {
            // BUG: Langsung menganggap data berhasil dibuat
            const tbody = document.getElementById('itemList');
            const emptyRow = document.getElementById('emptyRow');
            if (emptyRow) emptyRow.remove();

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${data.name}</td>
                <td>Rp ${data.price}</td>
                <td>${data.description}</td>
            `;
            tbody.appendChild(tr);
            form.reset();
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    });
});
