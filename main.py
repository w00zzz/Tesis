from catalogo_variables import crear_catalogo_base
from catalogo_variables import cargar_variables_prototipo
from tests import validar_catalogo
from utils import printdf

def main():
    catalogo1 = crear_catalogo_base()
    catalogo2 = cargar_variables_prototipo()

    # print(f"Columnas del catalogo base: {list(catalogo1.columns)}")
    printdf(catalogo2, "Catalogo de Variables")
    
    catalogo2.to_csv("output/catalogo_variables.csv", index=False)



if __name__ == "__main__":
    main()
