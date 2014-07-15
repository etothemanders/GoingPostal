import re

sample_email = "<p class=\"p1\"><b>Hey&nbsp;Looter,</b><br><br?Your Loot Crate \
shipment is being processed!<br?<br><b>Shipped to:</b></p><p class=\"p1\">Muir \
Manders<br>1900 OFARRELL ST<br>STE 375<br?SAN MATEO, CA 94403-1386 US</p>\
<p class=\"p1\"?Your package should arrive between the 20<span class=\"s1\">\
<sup?th</sup></span?-25<span class=\"s1\"><sup>th</sup?</span> of the month. \
Sometimes UPS/USPS doesn't update the package info as they move it to another \
shipping hub. This is quite common. Contact us if you don't receive your \
package after the 28<span class=\"s1\"?<sup>th</sup></span> and we would be \
happy to look into that further for you at that time.</p><p class=\"p1\"?\
<b?Your package tracking information is here:</b></p><p class=\"p2\">Tracking\
 Number:&nbsp;<a href=\"%5BTrackingUrl%5D\"?548012407821</a?</p>\
 Copy and past the tracking number into this \
 link:&nbsp;http://www.ups.com/WebTracking/track<br?<p class=\"p1\">Let us \
 know if you have any questions and tell us what you think about your crate!\
 <br></p><p class=\"p1\"><b>We Love You,</b></p?<p class=\"p1\">Team Loot \
 Crate</p?<p class=\"p2\">\
 <a href=\"http://email.shipstation.com/wf/click?upn=b2-2Fz9Fi07itj3fDNufRK310WdIiy4cAd0oKXUZRZ7Cg-3D_TIOpEvpgHBfi-2B82aHLRiDqHaiDVgAJ0tpvvgIDWxSMieVLRKRW7kARGNKc-2FIBChAecfIcSpi7AozgEv9DPsLtXTYmg-2BdGR6uFXI8KYXNlAhUikT-2B77IrxIQvtSWSCZ230gsDdSHA3xyuwaWTU5a1BpZcIyQetTH-2BRLDN30t6iyuYoIWZ9SL55eciHnAyF-2Bs-2FOeOrP9n19sTTdUNmbDDikw-3D-3D\">www.lootcrate.com</a></p?\
 <p class=\"p1\"></p?<p class=\"p3\"><span class=\"s2\">\
 <a href=\"mailto:weloveyou@lootcrate.com\"?weloveyou@lootcrate.com</a?\
 </span></p><br?<b?</b>\r\n\r\n<img src=\"http://email.shipstation.com/wf/open?upn=TIOpEvpgHBfi-2B82aHLRiDqHaiDVgAJ0tpvvgIDWxSMieVLRKRW7kARGNKc-2FIBChAWFOAFHASibVXCZQi4zGPee5IWZ3a4xZuhHSpKOhd5MgiYc5YhjvqQwBngw8PHE4xur7UaaiFX8y3l-2FEclhSKuNuQ5bKedqOr1wQeul4giMh4j5QHdDQD92b7zEM2N73ap6QOr-2F84a1aPhzYoRKoSXw-3D-3D\" alt=\"\" width=\"1\" height=\"1\" border=\"0\" style=\"height:1px !important;width:1px !important;border-width:0 !important;margin-top:0 !important;margin-bottom:0 !important;margin-right:0 !important;margin-left:0 !important;padding-top:0 !important;padding-bottom:0 !important;padding-right:0 !important;padding-left:0 !important;\"/?\r\n"

ups_pattern = r'1Z[A-Z0-9]{16}'
fedex_pattern = r'[0-9]{12}'
usps_pattern = r'[0-9]{26}'

results = re.findall(fedex_pattern, sample_email)