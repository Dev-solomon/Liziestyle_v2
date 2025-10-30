def order_template(order):
    # Generate product rows
    def generate_product_rows(products):
        product_rows = []
        for item in products:
            product_row = f"""
            <tr>
                <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                    <div style="margin-bottom: 5px; display:flex; align-items:center;">
                        <img loading="lazy" src="{item['images'][0]}" alt="{item['title']}" style="width: 60px; height: 60px; margin-top:10px; margin-right:10px; object-fit: cover;">
                        <div>
                            <p href="{order['orderUrl']}" style="color: #09d4fc;font-size:12px;">{item['title'].upper()}</p>
                            <p style="font-size:12px;">Variant : {item['variant']}</p>
                        </div>
                    </div>
                    <div style="border-bottom: 1px solid #edecec;"></div>
                </td>
            </tr>
            """
            product_rows.append(product_row)
        return ''.join(product_rows)

    # Generate total cost rows
    def generate_cost_rows(order):
        cost_rows = [
            {"label": "Totale parziale", "value": f"€{float(order['subTotal']):,.2f}"},
            {"label": "Costo di spedizione", "value": f"€{float(order['shippingCost']):,.2f}"},
            {"label": "Tassare", "value": f"€{float(order['taxPrice']):,.2f}"},
            {"label": "Totale", "value": f"€{float(order['totalPrice']):,.2f}"},
        ]
        
        cost_rows_html = []
        for cost in cost_rows:
            cost_row = f"""
            <tr>
                <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                    <div style="padding:20px 0">
                        <label style="font-size:15px">{cost['label']}</label>
                        <div style="font-weight: 600;font-size:13px;float:right">{cost['value']}</div>
                    </div>
                    <div style="border-bottom:1px solid #edecec;"></div>
                </td>
            </tr>
            """
            cost_rows_html.append(cost_row)
        return ''.join(cost_rows_html)


    # Full email template
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #e8ebe9; padding-top: 20px;">
        <tr>
            <td align="center">
                <div style="width: 100%; max-width: 650px; margin: 0 auto;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 650px; margin: 0 auto;">
                        <tbody>
                            <tr>
                                <td>
                                    <table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto; background: #ffffff;">
                                        <tbody>
                                            <tr>
                                                <td style="padding:70px 0px; background-color: #e9fff2">
                                                    <div style="text-align: center;">
                                                        <a href="{order['orderUrl']}" target="_blank" style="display: inline-block;">
                                                            <img loading="lazy" style="width: 100%; height: 70px;" src="https://res.cloudinary.com/dns8ckviy/image/upload/v1718299320/lizie_ctniwa.png" alt="liziestyle Logo">
                                                        </a>
                                                    </div>
                                                    <div style="color: #000000; font-size: 15px; font-family: Verdana, sans-serif; text-align: center;margin: 30px 0;">
                                                      Grazie per aver acquistato con noi. Ecco i dettagli del tuo ordine.
                                                    </div>
                                                    <div style="text-align: center;">
                                                        <button style="background-color: #09d4fc; width:27%; padding: 14px 0px; border: none; border-radius: 10px 10px; font-size: 15px; font-family: Verdana, sans-serif;">
                                                            <a href="{order['orderUrl']}" target="_blank" style="color: #ffffff; text-decoration: none;">
                                                                Visualizza ordine
                                                            </a>
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 2px solid #f1f0f0;">
                                                        <tbody>
                                                            <tr>
                                                                <td width="600" style="padding-top: 70px; padding-bottom: 40px; padding-left: 70px; padding-right: 70px;">
                                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                                        <tbody>
                                                                            {generate_product_rows(order["products"])}
                                                                            {generate_cost_rows(order)}
                                                                            <tr>
                                                                                <td height="50"></td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>
                                                                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td style="text-align: center;">
                                                                                                    <a href="https://www.linkedin.com/company/105483484" target="_blank" style="display: inline-block; margin-left: 3px; margin-right: 3px;">
                                                                                                       <img loading="lazy" width="48" height="48" src="https://img.icons8.com/fluency/48/linkedin.png" alt="linkedin"/> 
                                                                                                    </a>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <div style="width: 100%; max-width: 620px; margin: 0 auto;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="font-family: Verdana, sans-serif; font-weight: normal; font-size: 10px; line-height: 24px; color: black; text-align: left;  padding: 15px 15px;">
                                Copyright © 2023 <a href="https://www.liziestyle.com" target="_blank" style="text-decoration: none; color: #09d4fc">{order["siteName"]}</a>
                            </td>
                            <td style="font-family: Verdana, sans-serif; font-weight: normal; font-size: 10px; line-height: 24px; color: black; text-align: right;  padding: 15px 15px;">
                                Offerto da <a href="https://www.linkedin.com/company/105483484" target="_blank" style="text-decoration: none; color: #09d4fc;">{order["siteName"]} Azienda</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
    """

    


