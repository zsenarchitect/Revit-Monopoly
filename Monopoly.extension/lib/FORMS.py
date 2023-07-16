



def dialogue( title = "Monopoly",
            main_text = "main_text",
            sub_text = None,
            options = None,

            footer_text = "Sen Zhang Game Studio",
           
            expended_content = None,
            extra_check_box_text = None,
            verification_check_box_text = None,
            icon = "info"):

    """
    extra check box appear before commands options
    verification_check_box_text appear after commands options
    is activaed, the result of dialogue will return a tuple of two values.

    options = [["opt 1","description long long long long"], ["opt 2"]]   if options is a string, then used as main text, but if it is a list of two strings, the second string will be used as description. In either case, the command link will return main text


    TaskDialogIconNone,	No icon.
    TaskDialogIconShield,	Shield icon.
    TaskDialogIconInformation,	Information icon.
    TaskDialogIconError,	Error icon.
    TaskDialogIconWarning, Warning icon
    """
    def result_append_checkbox_result(res):
        try:
            extra_checkbox_status = main_dialog.WasExtraCheckBoxChecked ()
            return res, extra_checkbox_status #extra_checkbox_status:{}".format(extra_checkbox_status)
        except:
            pass
        try:
            verification_checkbox_status = main_dialog.WasVerificationChecked  ()

            return res , verification_checkbox_status #"#verification_checkbox_status:{}".format(verification_checkbox_status)
        except:
            pass
        return res


    """
    if not is_SZ():
        return
    """
    from Autodesk.Revit import UI
    main_dialog = UI.TaskDialog(title)
    main_dialog.MainInstruction = main_text
    main_dialog.MainContent = sub_text
    main_dialog.TitleAutoPrefix = False
  
    main_dialog.FooterText = footer_text

    if extra_check_box_text is not None:
        main_dialog.ExtraCheckBoxText  = extra_check_box_text
    else:
        if verification_check_box_text is not None:
            main_dialog.VerificationText   = verification_check_box_text
    main_dialog.ExpandedContent  = expended_content

    from pyrevit.coreutils import get_enum_values
    if options:
        clinks = get_enum_values(UI.TaskDialogCommandLinkId)
        max_clinks = len(clinks)
        for idx, cmd in enumerate(options):
            if idx < max_clinks:
                if isinstance(cmd, list):
                    main_dialog.AddCommandLink(clinks[idx], cmd[0], cmd[1])
                else:
                    main_dialog.AddCommandLink(clinks[idx], cmd)

    if icon == "shield":
        main_dialog.MainIcon = UI.TaskDialogIcon.TaskDialogIconShield
    elif icon == "warning":
        main_dialog.MainIcon = UI.TaskDialogIcon.TaskDialogIconWarning
    elif icon == "error":
        main_dialog.MainIcon = UI.TaskDialogIcon.TaskDialogIconError
    elif icon == "info":
        main_dialog.MainIcon = UI.TaskDialogIcon.TaskDialogIconInformation
    res = main_dialog.Show()


    if res == UI.TaskDialogResult.Close:
        res = "Close"
    if res == UI.TaskDialogResult.Cancel:
        res = "Cancel"


    if 'CommandLink' in str(res):
        tdresults = sorted([x for x in get_enum_values(UI.TaskDialogResult) if 'CommandLink' in str(x)])
        residx = tdresults.index(res)
        if isinstance(options[residx], list):
            res = options[residx][0]
        else:
            res = options[residx]


    return result_append_checkbox_result(res)


