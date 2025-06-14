import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Sidebar instructions
st.sidebar.title("Petunjuk Penggunaan")
st.sidebar.markdown("""
Pilih salah satu tab di atas untuk mengeksplorasi model matematika berikut:

1. **Optimasi Produksi (Linear Programming)**
2. **Model Persediaan (EOQ)**
3. **Model Antrian (M/M/1)**
4. **Break-Even Point Analysis**

Masukkan parameter yang dibutuhkan, lalu lihat hasil analisis dan visualisasinya.
""")

# Tab Navigation
tabs = st.tabs(["Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Break-Even Point"])

# Tab 1: Optimasi Produksi
with tabs[0]:
    st.header("Optimasi Produksi (Linear Programming)")
    st.markdown("Gunakan metode simpleks untuk memaksimalkan keuntungan.")
    
    c1 = st.number_input("Keuntungan per unit produk A", value=40)
    c2 = st.number_input("Keuntungan per unit produk B", value=30)
    a1 = st.number_input("Jam kerja per unit produk A", value=2)
    a2 = st.number_input("Jam kerja per unit produk B", value=1)
    b1 = st.number_input("Batas maksimum jam kerja", value=100)

    if st.button("Hitung Optimasi"):
        res = linprog(c=[-c1, -c2], A_ub=[[a1, a2]], b_ub=[b1], method='highs')
        if res.success:
            x = res.x
            st.success(f"Produksi optimal: Produk A = {x[0]:.2f}, Produk B = {x[1]:.2f}")
            st.info(f"Total keuntungan: Rp {-res.fun:.2f}")
            fig, ax = plt.subplots()
            ax.bar(['Produk A', 'Produk B'], x, color=['skyblue', 'salmon'])
            ax.set_ylabel("Unit Produksi")
            st.pyplot(fig)
        else:
            st.error("Optimasi gagal dilakukan.")

# Tab 2: EOQ
with tabs[1]:
    st.header("Model Persediaan (EOQ)")
    D = st.number_input("Permintaan Tahunan (D)", value=1000)
    S = st.number_input("Biaya Pemesanan per Order (S)", value=50)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=2)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ = {EOQ:.2f} unit/order")
        q = np.linspace(1, 2*EOQ, 100)
        total_cost = (D/q)*S + (q/2)*H
        fig, ax = plt.subplots()
        ax.plot(q, total_cost, label='Total Cost')
        ax.axvline(EOQ, color='r', linestyle='--', label='EOQ')
        ax.set_xlabel('Order Quantity')
        ax.set_ylabel('Total Cost')
        ax.legend()
        st.pyplot(fig)

# Tab 3: Antrian M/M/1
with tabs[2]:
    st.header("Model Antrian (M/M/1)")
    lambd = st.number_input("Tingkat Kedatangan (λ)", value=2.0)
    mu = st.number_input("Tingkat Pelayanan (μ)", value=3.0)

    if 0 < lambd < mu:
        rho = lambd / mu
        Lq = rho**2 / (1 - rho)
        Wq = Lq / lambd
        st.success(f"Utilisasi server (ρ): {rho:.2f}")
        st.info(f"Jumlah rata-rata pelanggan dalam antrian (Lq): {Lq:.2f}")
        st.info(f"Waktu rata-rata menunggu dalam antrian (Wq): {Wq:.2f} jam")

        x = np.arange(1, 11)
        prob = (1 - rho) * rho**x
        fig, ax = plt.subplots()
        ax.bar(x, prob)
        ax.set_xlabel('Jumlah pelanggan dalam sistem')
        ax.set_ylabel('Probabilitas')
        st.pyplot(fig)
    else:
        st.warning("Pastikan λ < μ agar sistem stabil.")

# Tab 4: Break-Even Point
with tabs[3]:
    st.header("Break-Even Point Analysis")
    FC = st.number_input("Biaya Tetap (Fixed Cost)", value=10000)
    VC = st.number_input("Biaya Variabel per Unit", value=20)
    P = st.number_input("Harga Jual per Unit", value=50)

    if P > VC:
        BEP = FC / (P - VC)
        st.success(f"Break-Even Point: {BEP:.2f} unit")
        q = np.linspace(0, BEP*2, 100)
        total_cost = FC + VC * q
        total_revenue = P * q

        fig, ax = plt.subplots()
        ax.plot(q, total_cost, label='Total Cost')
        ax.plot(q, total_revenue, label='Total Revenue')
        ax.axvline(BEP, color='red', linestyle='--', label='Break-Even Point')
        ax.set_xlabel('Quantity')
        ax.set_ylabel('Cost / Revenue')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Harga jual harus lebih besar dari biaya variabel untuk menghitung BEP.")
