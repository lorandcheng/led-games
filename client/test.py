if __name__ == "__main__":
    output = []
    for r in range(32):
        output.append([])
        for c in range(32):
            if r == 0 or r == 31 or c == 0 or c == 31:
                output[r].append(1)
            else:
                output[r].append(0)
    print(output)