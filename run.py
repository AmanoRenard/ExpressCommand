from screen_operator.core import ScreenOperator

operator = ScreenOperator(confidence=0.85, move_duration=0.01)
operator.execute_workflow(
    open_address_img="OpenAddress.png",
    copy_imgs=["CopyAddress1.png", "CopyAddress2.png", "ClickCopy.png"],
    right_panel_width=1900
)