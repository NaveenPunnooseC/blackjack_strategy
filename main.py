import f

strategymap = {
    "standardstrategy": f.standardstrategy,
    "dealerstrategy": f.dealerstrategy,
    "randomstrategy": f.randomstrategy,
    "onehit": f.onehit,
    "greaterthandealer": f.greaterthandealer
}

print("\n".join(strategymap.keys()))
print()

while True:
    strategyname = input("Which strategy would you like to test?: ")
    if strategyname in strategymap:
        break
    else:
        print("That is not a strategy. Please put a real one")

while True:
    times = input("How many times would you like to run the sim?: ")
    if times.isdigit():
        times = int(times)
        if times > 0:
            break
    print("Please enter a natural number")

strategy = strategymap[strategyname]
print("\nChoose mode:")
print("1 - Single simulation")
print("2 - Distribution experiment")
print()

while True:
    mode = input("Select mode (1 or 2): ")
    if mode in ("1", "2"):
        break
    print("Please enter 1 or 2")

if mode == "1":
    print(f.runsim(times, strategy))

else:
    while True:
        nsims = input("How many simulations?: ")
        if nsims.isdigit() and int(nsims) > 0:
            nsims = int(nsims)
            break
        print("Please enter a natural number")

    results = f.runmanysims(nsims, times, strategy)

    print("\n--- Distribution Results ---")
    print(f"Mean win %: {results['mean_win%']:.3f}")
    print(f"Standard deviation: {results['std_dev']:.3f}")
    print(f"Min win %: {results['min_win%']:.3f}")
    print(f"Max win %: {results['max_win%']:.3f}")

