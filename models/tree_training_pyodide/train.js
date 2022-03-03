var promises = [
  languagePluginLoader,
  $.get("../../data/rob_data.csv")
]

console.log("training")

Promise.all(promises)
  .then((data) => {
    window.data = data[1]
    pyodide.loadPackage(['numpy', 'scikit-learn', 'pandas']).then(() => {
          pyodide.runPython(pythonCode)
      })
  })
