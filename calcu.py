
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, sympify,limit,diff,integrate,latex
#la wea para los pdf
from reportlab.platypus import(
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
#barra lateral por si quiero cambiar
st.set_page_config(page_title="Calculadora Matemática Completa", layout="wide")
st.sidebar.title(" Menú Principal")
menu = st.sidebar.radio(
    "Seleccione una opción",
    ["Inicio", "Límites", "Integrales", "Geometría Analítica"]
)

# wea de funcion de los pdf 
x = symbols("x")
def generar_pdf(
        titulo,
        funcion,
        procedimiento,
        resultado,
        imagen="grafico.png"
):
    pdf = "resultado.pdf"
    doc = SimpleDocTemplate(pdf)
    estilos = getSampleStyleSheet()
    contenido = []
    contenido.append(
        Paragraph(
            titulo,
            estilos["Title"]
        )
    )
    contenido.append(
        Paragraph(
            f"Función: {funcion}",
            estilos["BodyText"]
        )
    )
    contenido.append(
        Paragraph(
            "Procedimiento",
            estilos["Heading2"]
        )
    )
    contenido.append(
        Paragraph(
            procedimiento,
            estilos["BodyText"]
        )
    )
    contenido.append(
        Paragraph(
            f"Resultado: {resultado}",
            estilos["BodyText"]
        )
    )
    contenido.append(
        Spacer(1,12)
    )
    try:
        contenido.append(
            Image(
                imagen,
                width=350,
                height=250
            )
        )
    except:
        pass
    doc.build(contenido)
    return pdf
#menu de inicio
if menu == "Inicio":
    st.title(" Calculadora Matemática Completa")
    col1,col2,col3=st.columns(3)
    with col1:
        st.image(r"C:\Users\mp1318\Desktop\weas de c++\limites.jpg")
        st.caption("LIMITES")
    with col2:
        st.image(r"C:\Users\mp1318\Desktop\weas de c++\inte.png",width=400)
        st.caption("INTEGRALES") 
    with col3:
        st.image(r"C:\Users\mp1318\Desktop\weas de c++\geo.png",width=700)
        st.caption("GEOMETRIA ANALITICA")      
    
# seccion de limites
elif menu == "Límites":
    st.title("Límites y Regla de L'Hôpital")
#donde selecciono cual
    metodo = st.selectbox(
        "Seleccione el caso",
        ["Límite Directo", "L'Hôpital 0/0", "L'Hôpital ∞/∞", "L'Hôpital Repetido"]
    )
#donde se coloca los ejercicios
    expr = st.text_input("Función", "sin(x)/x")
    punto_txt = st.text_input("Punto", "0")
    zoom=st.slider(
        "zoom del grafico",
        min_value=1,
        max_value=20,
        value=5
    )

    if st.button("Resolver límite"):
        try:
            f = sympify(expr)
            punto = sympify(punto_txt)
            st.subheader("Procedimiento")

            if metodo == "Límite Directo":
                resultado = limit(f, x, punto)
                st.latex(latex(resultado))
#pasos para resolver
            else:
                num, den = f.as_numer_denom()
                st.subheader("Expresion original")
                st.latex(r"\frac{%s}{%s}"%(
                    latex(f.as_numer_denom()[0]),
                    latex(f.as_numer_denom()[1])
                ))
                st.subheader("Evaluacion de un punto")
                valor_num= num.subs(x,punto)
                valor_den= num.subs(x,punto)
                st.latex(r"\frac{%s}{%s}"%(latex(valor_num),latex(valor_den)))
                st.write("Numerador")
                st.latex(latex(num))
                st.write("Denominador")
                st.latex(latex(den))
                st.subheader("Aplicacion de L.Hopital")
                for i in range(1, 6):
                    num = diff(num, x)
                    den = diff(den, x)
                    st.write(f"Paso {i}")
                    st.latex(r"\frac{%s}{%s}" % (latex(num), latex(den)))
                    try:
                        resultado=limit(num/den,x,punto)
                        if resultado not in(sp.nan,sp.zoo):
                            break
                    except:
                        pass
                resultado = limit(num / den, x, punto)
            st.success(f"Resultado = {resultado}")
            st.subheader("resultado final")
            st.latex(latex(resultado    ))
# parte del grafico
            try:
                f_num = sp.lambdify(x, f, "numpy")
                #parte para el slider
                xs = np.linspace(
                    float(punto)-zoom,
                    float(punto)+zoom,
                    1000                    
                )
                #hasta aca el slider webada esa
                ys = f_num(xs)
                fig, ax = plt.subplots()
                ax.plot(xs, ys)
                ax.axvline(float(punto), linestyle="--")
                ax.grid(True)
                ax.set_title("Gráfico del límite")
                st.pyplot(fig)
            except:
                pass
        except Exception as e:
            st.error(str(e))
#seccion de integrales
elif menu == "Integrales":
    st.title("Integrales con gráfico")
    expr = st.text_input("Función a integrar", "x**2")
    if st.button("Integrar"):
        try:
            f = sympify(expr)
            integral = integrate(f, x)
            st.subheader("Resultado")
            st.latex(latex(integral))
            f_num = sp.lambdify(x, f, "numpy")
            xs = np.linspace(-5, 5, 500)
            ys = f_num(xs)
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.fill_between(xs, ys, alpha=0.3)
            ax.grid(True)
            ax.set_title("Representación gráfica")
            fig.savefig("grafico.png")
            st.pyplot(fig)
            #wea del pdf
            procedimiento=f"""
            Funcion original:{expr}
            Integral calculada:
            {integral}
            """
            pdf=generar_pdf(
                "Integral",
                expr,
                procedimiento,
                integral
            )
            with open(pdf,"rb") as archivo:
                st.download_button("descargar wea",archivo,file_name="integral.pdf")
        except Exception as e:
            st.error(str(e))
#geometria analitica seccion
elif menu == "Geometría Analítica":
    st.title("Geometría Analítica")

    tema = st.selectbox(
        "Tema",
        [
            "Distancia entre dos puntos",
            "Punto Medio",
            "Pendiente",
            "Recta Punto-Pendiente",
            "Circunferencia",
            "Parabola",
            "Elipse",
            "Hiperbola"
        ]
    )

    if tema == "Distancia entre dos puntos":
        x1 = st.number_input("x1")
        y1 = st.number_input("y1")
        x2 = st.number_input("x2")
        y2 = st.number_input("y2")
        if st.button("Calcular"):
            d = ((x2-x1)**2 + (y2-y1)**2)**0.5
            st.success(f"Distancia = {d}")
            fig, ax = plt.subplots()
            ax.scatter([x1,x2],[y1,y2])
            ax.plot([x1,x2],[y1,y2])
            ax.grid(True)
            st.pyplot(fig)

    elif tema == "Punto Medio":
        x1 = st.number_input("x1 ")
        y1 = st.number_input("y1 ")
        x2 = st.number_input("x2 ")
        y2 = st.number_input("y2 ")

        if st.button("Mostrar"):
            mx = (x1+x2)/2
            my = (y1+y2)/2
            st.success(f"M = ({mx}, {my})")
            fig, ax = plt.subplots()
            ax.scatter([x1,x2,mx],[y1,y2,my])
            ax.plot([x1,x2],[y1,y2])
            ax.grid(True)
            st.pyplot(fig)

    elif tema == "Pendiente":
        x1 = st.number_input("x1  ")
        y1 = st.number_input("y1  ")
        x2 = st.number_input("x2  ")
        y2 = st.number_input("y2  ")

        if st.button("Resolver"):
            m = (y2-y1)/(x2-x1)
            st.success(f"Pendiente = {m}")

            fig, ax = plt.subplots()
            ax.scatter([x1,x2],[y1,y2])
            ax.plot([x1,x2],[y1,y2])
            ax.grid(True)
            st.pyplot(fig)

    elif tema == "Recta Punto-Pendiente":
        x1 = st.number_input("x₁")
        y1 = st.number_input("y₁")
        m = st.number_input("Pendiente")

        if st.button("Graficar recta"):
            xs = np.linspace(-20,20,500)
            ys = m*(xs-x1)+y1
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.scatter([x1],[y1])
            ax.grid(True)
            st.pyplot(fig)

    elif tema == "Circunferencia":
        h = st.number_input("Centro h")
        k = st.number_input("Centro k")
        r = st.number_input("Radio", value=1.0)

        if st.button("Graficar circunferencia"):
            t = np.linspace(0, 2*np.pi, 500)
            xs = h + r*np.cos(t)
            ys = k + r*np.sin(t)
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.scatter([h],[k])
            ax.axis("equal")
            ax.grid(True)
            st.pyplot(fig)
    elif tema == "Parábola":
     a = st.number_input("a", value=1.0)
     b = st.number_input("b", value=0.0)
     c = st.number_input("c", value=0.0)
    if st.button("Graficar parábola"):
        x_vals = np.linspace(-10, 10, 500)
        y_vals = a*x_vals**2 + b*x_vals + c
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label="Parábola")
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    elif tema == "Elipse":
     a = st.number_input("Semieje a", value=5.0)
     b = st.number_input("Semieje b", value=3.0)
    if st.button("Graficar elipse"):
        t = np.linspace(0, 2*np.pi, 500)
        x_vals = a * np.cos(t)
        y_vals = b * np.sin(t)
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.scatter([0], [0], color="red")
        ax.set_aspect("equal")
        ax.grid(True)
        st.pyplot(fig)
    elif tema == "Hipérbola":
     a = st.number_input("a", value=2.0)
     b = st.number_input("b", value=1.0)
    if st.button("Graficar hipérbola"):
        x_vals = np.linspace(-10, 10, 1000)
        x_vals = x_vals[np.abs(x_vals) > a]  # evita dominio inválido
        y_vals_pos = b * np.sqrt((x_vals*2 / a*2) - 1)
        y_vals_neg = -y_vals_pos
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals_pos)
        ax.plot(x_vals, y_vals_neg)
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.grid(True)
        st.pyplot(fig)