print(fechas)
      fig, ax = plt.subplots()
      ax.plot(fechas, altos, color = 'tab:purple', label = 'Altos')
      ax.plot(fechas, medios, color = 'tab:green', label = 'Medio')
      ax.plot(fechas, bajos, color = 'tab:red', label = 'Bajos')
      ax.set_ylim([-1,1])
      ax.legend(loc = 'upper right')
      ax.set_xlabel("Fechas")
      ax.set_ylabel("Valor")
      ax.grid()
      plt.show()