def sidebar_link(label: str) -> str:
    """Return an XPath for a sidebar link identified by its accessible label."""
    return f"//a[@aria-label='{label}']"


def text_button(label: str) -> str:
    """Return an XPath for a button with normalized visible text."""
    return f"//button[normalize-space()='{label}']"


def labeled_input(label: str, placeholder: str = "Enter") -> str:
    """Return the first input following a form label prefix."""
    return (
        f"(//*[starts-with(normalize-space(), '{label}')]"
        f"/following::input[@placeholder='{placeholder}'])[1]"
    )


def labeled_select(label: str) -> str:
    """Return the first native select following a form label prefix."""
    return (
        f"(//*[starts-with(normalize-space(), '{label}')]"
        "/following::select[1])[1]"
    )
