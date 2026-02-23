from utils import cargar_variables_prototipo
from utils import printdf
from utils import cargar_csv

def main():
    # catalogo2 = cargar_variables_prototipo()

    # printdf(catalogo2, "Catalogo de Variables")
    
    # catalogo2.to_csv("output/catalogo_variables.csv", index=False)
    csv = cargar_csv("output/catalogo_variables.csv")
    printdf(csv, "Catalogo de Variables")


if __name__ == "__main__":
    main()
