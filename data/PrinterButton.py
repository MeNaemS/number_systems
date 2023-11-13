from data.QObjects import PushButton


# The Button class inherits from the PushButton class. Sets the button style for the print window.
class Button(PushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(
            'border-width: 1px;'
            'border-style: solid;'
            'border-radius: 10px;'
            'border-color: rgba(76, 195, 253, 0.8);'
            'background-color: rgba(76, 195, 253, 0.8);'
            'font-weight: bold;'
            'font-size: 17px;'
            'color: White;'
        )
