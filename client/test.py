if __name__ == "__main__":
    import outputs
    from games import checkers
    output = outputs.TerminalDisplay()
    checkers = checkers.Checkers(output)
    print(type(checkers.output).__name__)