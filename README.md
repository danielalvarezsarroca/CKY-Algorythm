# CKY-Algorythm
# Pràctica de Programació i Algorísmia Avançada – CKY

## Descripció
Aquest projecte implementa l’**algorisme determinista Cocke–Kasami–Younger (CKY)** en Python, utilitzat per a l’anàlisi sintàctica de cadenes i la verificació de pertinença a un llenguatge generat per una **gramàtica lliure de context (CFG)** en **Forma Normal de Chomsky (CNF)**.

El programa rep com a entrada una gramàtica en CNF i una paraula, i retorna un valor booleà:
- `True` → si la paraula pertany al llenguatge generat per la gramàtica.  
- `False` → en cas contrari.

## Característiques
- **Entrada**:  
  - Gramàtica en CNF.  
  - Paraula a comprovar.  
  - Format lliure per a ambdós.  
- **Sortida**:  
  - Booleà (`True` / `False`) indicant la pertinença al llenguatge.  
- **Execució**:  
  - Programa principal des d’on es poden carregar diferents gramàtiques i paraules.  
- **Codi documentat**:  
  - Es proporcionen comentaris explicatius a les parts més rellevants.  
- **Tests inclosos**:  
  - Es subministren diversos jocs de proves complets per validar l’algorisme.

## Exemples de gramàtiques (CNF)
El repositori inclou exemples de gramàtiques de prova com:  
- **G1** i **G2**, proporcionades a l’enunciat de la pràctica, que permeten verificar el correcte funcionament de l’algorisme CKY.

## Extensions opcionals
A més de la implementació bàsica, es poden afegir les funcionalitats següents:  
1. Transformació de qualsevol CFG a CNF.  
2. Versió probabilística de l’algorisme CKY.  

