=========================================
Data Parsing, Analysis, and Visualization
=========================================

Reading and visualizing data from a ProCoDA data file
-----------------------------------------------------
.. code:: python
  
    import aguaclara as ac
    from aguaclara.core.units import u
    import matplotlib.pyplot as plt
    
    path = "https://raw.githubusercontent.com/AguaClara/team_resources/master/Data/datalog%206-14-2018.xls"

    time = ac.column_of_time(path=path, start=2250, end=5060).to(u.hr)
    influent_turbidity = ac.column_of_data(path=path, start=2250, column=3, end=5060)
    effluent_turbidity = ac.column_of_data(path=path, start=2250, column=4, end=5060)

    # set up multiple subplots with same x-axis
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # make the first subplot (Effluent Turbidity vs Time)
    ax1.set_xlabel("Time (hours)")
    ax1.set_ylabel("Effluent Turbidity (NTU)")
    line1, = ax1.plot(time, effluent_turbidity, color="blue")

    # make the second subplot (Influent Turbidity vs Time)
    ax2.set_ylabel("Influent Turbidity (NTU)")
    ax2.set_ylim(60,120)
    line2, = ax2.plot(time, influent_turbidity, color="green")

    plt.legend((line1, line2), ("Effluent", "Influent"))
