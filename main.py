import pywavefront
import os

mobile = False
file = 'file.obj'
outputMats = True



scene = pywavefront.Wavefront(
  file,
  collect_faces=True,
)

#add latex for [ ] depending on device
def latexBrackets(str):
  if (mobile):
    return "\\left[" + str + "\\right]"
  else:
    return "\\\\left[" + str + "\\\\right]"

#variable initialization
x = z = y = p1 = p2 = p3 = ""

#set vertex indeces for faces
for face in scene.mesh_list[0].faces:
  p1 += (str(face[0]+1) + ",")
  p2 += (str(face[1]+1) + ",")
  p3 += (str(face[2]+1) + ",")


print(scene.mesh_list[0].faces[6])
#remove last ,
p1 = p1[:-1]
p2 = p2[:-1]
p3 = p3[:-1]

#set x z and y of all vertices
for vertex in scene.vertices:
  x += (str(vertex[0]) + ",")
  z += (str(vertex[2]) + ",")
  y += (str(vertex[1]) + ",")

#remove last ,
x = x[:-1]
z = z[:-1]
y = y[:-1]

#add latex brackets
x=latexBrackets(x)
z=latexBrackets(z)
y=latexBrackets(y)
p1=latexBrackets(p1)
p2=latexBrackets(p2)
p3=latexBrackets(p3)

#code to enter variable depending on device
def code(var,varLatex):
  if (mobile):
    return "javascript:Calc.setExpression({latex:String.raw`" + varLatex + "=" + var + "`});"
  else: 
    return "let myState = Calc.getState(); myState.expressions.list.find(e => e.latex ? e.latex.startsWith('" + varLatex + "=') : false).latex = '" + varLatex + "=" + var + "';Calc.setState(myState);"

#add code string to variables
x=code(x,"X_{0}")
z=code(z,"Z_{0}")
y=code(y,"Z_{0}")
p1=code(p1,"P_{1}")
p2=code(p2,"P_{2}")
p3=code(p3,"P_{3}")

#function to make a file and write a variable to it
def writeFile(path,value):
  if os.path.exists(path):
    os.remove(path)
  file = open(path, "a")
  file.write(value)
  file.close()

#folder where output text goes
textFilesFolder = "Text_files/"

#write to each file
writeFile((textFilesFolder+"x.txt"),x)
writeFile((textFilesFolder+"z.txt"),z)
writeFile((textFilesFolder+"y.txt"),y)
writeFile((textFilesFolder+"p1.txt"),p1)
writeFile((textFilesFolder+"p2.txt"),p2)
writeFile((textFilesFolder+"p3.txt"),p3)



#material parsing
if outputMats:
  parsed = []
  with open(file, 'r') as f:
      for line in f:
        if line.startswith("f "):
          for i in range(len(line[2:].split())-2):
            parsed.append("face")
        elif line.startswith("usemtl"):
          parsed.append(line.replace("\n",""))
        else:
          parsed.append("other")

  faceMat = [
    next(i[7:] for i in reversed(parsed[:index]) if i.startswith("usemtl"))
    for index, item in enumerate(parsed) if item == "face"
  ]
  #defined name for each material
  matNames = [mat.name for mat in scene.mesh_list[0].materials]
  matValues = ','.join([str(matNames.index(mat)+1) for mat in faceMat])
  matString =code(latexBrackets(matValues),"M")
  writeFile((textFilesFolder+"materials.txt"),matString)