import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Aplikasi Pemecahan Masalah Statistik", layout="wide")
st.title("Aplikasi Pemecahan Masalah Statistik")

# Tab navigasi
menu = ["Statistik Deskriptif", "Uji Hipotesis", "Regresi Linear", "Visualisasi Data"]
choice = st.sidebar.selectbox("Pilih fitur", menu)

# 1. Statistik Deskriptif
if choice == "Statistik Deskriptif":
    st.header("Statistik Deskriptif")
    st.write("Masukkan data secara manual (pisahkan dengan koma atau spasi)")
    data_input = st.text_area("Masukkan data:")

    if data_input:
        data = pd.Series([float(x) for x in data_input.replace(',', ' ').split()])
        st.write("Data yang dimasukkan:", data.tolist())

        if st.button("Hitung Statistik Deskriptif"):
            stats_result = data.describe()
            st.write("Statistik Deskriptif:")
            st.write(stats_result)

# 2. Uji Hipotesis
elif choice == "Uji Hipotesis":
    st.header("Uji Hipotesis")
    st.write("Masukkan data untuk kolom pertama (pisahkan dengan koma atau spasi)")
    data_input1 = st.text_area("Masukkan data kolom pertama:")
    test_type = st.selectbox("Pilih jenis uji", ["Uji t satu sampel", "Uji t dua sampel", "Uji ANOVA"])

    if data_input1:
        data1 = pd.Series([float(x) for x in data_input1.replace(',', ' ').split()])
        st.write("Data Kolom Pertama:", data1.tolist())

        if test_type == "Uji t satu sampel":
            pop_mean = st.number_input("Masukkan nilai rata-rata populasi")
            if st.button("Lakukan Uji t satu sampel"):
                t_stat, p_val = stats.ttest_1samp(data1, pop_mean)
                st.write(f"Hasil Uji t satu sampel:\nT-statistik: {t_stat}, p-value: {p_val}")

        elif test_type == "Uji t dua sampel":
            st.write("Masukkan data untuk kolom kedua (pisahkan dengan koma atau spasi)")
            data_input2 = st.text_area("Masukkan data kolom kedua:")
            if data_input2:
                data2 = pd.Series([float(x) for x in data_input2.replace(',', ' ').split()])
                st.write("Data Kolom Kedua:", data2.tolist())
                if st.button("Lakukan Uji t dua sampel"):
                    t_stat, p_val = stats.ttest_ind(data1, data2)
                    st.write(f"Hasil Uji t dua sampel:\nT-statistik: {t_stat}, p-value: {p_val}")

        elif test_type == "Uji ANOVA":
            st.write("Masukkan data untuk masing-masing grup (pisahkan dengan koma atau spasi)")
            group_data_input = st.text_area("Masukkan data grup, pisahkan grup dengan baris baru:")
            if group_data_input:
                group_data = [pd.Series([float(x) for x in group.replace(',', ' ').split()]) for group in group_data_input.splitlines() if group.strip()]
                if st.button("Lakukan Uji ANOVA"):
                    f_stat, p_val = stats.f_oneway(*group_data)
                    st.write(f"Hasil Uji ANOVA:\nF-statistik: {f_stat}, p-value: {p_val}")

# 3. Regresi Linear
elif choice == "Regresi Linear":
    st.header("Regresi Linear")
    st.write("Masukkan data untuk variabel X (pisahkan dengan koma atau spasi)")
    x_input = st.text_area("Masukkan data X:")
    st.write("Masukkan data untuk variabel Y (pisahkan dengan koma atau spasi)")
    y_input = st.text_area("Masukkan data Y:")

    if x_input and y_input:
        x = np.array([float(x) for x in x_input.replace(',', ' ').split()])
        y = np.array([float(y) for y in y_input.replace(',', ' ').split()])

        if len(x) == len(y):
            st.write("Data X:", x.tolist())
            st.write("Data Y:", y.tolist())

            if st.button("Hitung Regresi Linear"):
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                st.write(f"Persamaan regresi: Y = {slope:.2f}X + {intercept:.2f}")
                st.write(f"Koefisien Determinasi (R^2): {r_value**2:.2f}")

                # Visualisasi
                plt.scatter(x, y, label="Data", color="blue")
                plt.plot(x, slope * x + intercept, label="Regresi", color="red")
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.legend()
                st.pyplot(plt)
        else:
            st.warning("Data X dan Y harus memiliki panjang yang sama.")

# 4. Visualisasi Data
elif choice == "Visualisasi Data":
    st.header("Visualisasi Data")
    st.write("Masukkan data untuk visualisasi (pisahkan dengan koma atau spasi)")
    data_input = st.text_area("Masukkan data:")

    if data_input:
        data = pd.Series([float(x) for x in data_input.replace(',', ' ').split()])
        st.write("Data yang dimasukkan:", data.tolist())

        plot_type = st.selectbox("Pilih jenis visualisasi", ["Histogram", "Boxplot"])

        if plot_type == "Histogram":
            bins = st.slider("Jumlah bins", min_value=5, max_value=50, value=10)
            if st.button("Tampilkan Histogram"):
                plt.hist(data, bins=bins, color="skyblue", edgecolor="black")
                plt.xlabel("Data")
                plt.ylabel("Frekuensi")
                st.pyplot(plt)

        elif plot_type == "Boxplot":
            if st.button("Tampilkan Boxplot"):
                plt.boxplot(data)
                plt.ylabel("Data")
                st.pyplot(plt)