Below is an example ```headers``` :

| Header name | Header value |
| ----------- | ------------ |
| Delivered-To | amrulloev.subhon@gmail.com |
| Received | by 2002:ac8:5a4e:0:0:0:0:0 with SMTP id o14csp1598582qta;        Fri, 21 May 2021 18:29:48 -0700 (PDT) |
| X-Received | by 2002:ac8:6908:: with SMTP id e8mr14647271qtr.174.1621646988482;        Fri, 21 May 2021 18:29:48 -0700 (PDT) |
| ARC-Seal | i=1; a=rsa-sha256; t=1621646988; cv=none;        d=google.com; s=arc-20160816;        b=nk0ZFXEDOHC4Ku9rDRuh4qdErYF8ydWObvezHIJRwJb2nb33Mx7QlI2n4V6vm0VkZT         7DdYUxBSAukiJBZQKm5WGUYQ/5wKqE4VTGW0LiDJGkZ70i4yRDVDlIKIGzWH+3AePBy0         bTiMZgxVGUhcJsdKbAUPP7nnmRbtDsULppbFdJ8ZjWsxzObrPFVg6GhWcKe6BJ9bLos7         EzYDJEEvbc3qg+q6t1S8hljDBRMYJlIO9gPhKhBaRiA3s6HA9y/3X5kMQ0UthsUfbtb8         3unWtK0SxgvGZ4yGDxdPTV2iQCIUxqmqszPcHhrR1FzFsQ7T72lw7d2wAFLIvAQ5ySIa         Dj9w== |
| ARC-Message-Signature | i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=to:from:subject:message-id:feedback-id:date:mime-version         :dkim-signature;        bh=4J4MOmQFvdqoF4iFFRFRsqKqHvOKXhnARkiTad9G+EA=;        b=m0OjeRIa+x01isW7qqu+sg1Vo4OFrkqrPVDpoSGazKgem8hjZi/xHZvb2TOSE1/qTB         JVAHN0wbdRol2rH5pXMoorxdEtjvhufrzC13IK+OKPxL9gPqHLTR21KqUEWNsaoeFyPz         N4P0V2lJEDeEQL59ZYHDvUQyBFEzvGOBm6+dORFRbCA0azdRgocSMdvxQMU0V4c344gi         dGD6y67VAASFPiMNP60kv0SS+4kvjrM+0McbcRaSJ1ybsyRynvH6xHpUYLK/2nTY7HSy         Raj0Ci1a8BBigFSjgv72bGKYcE0aU/50sdgKUHtfYA80VMDAhZpDUz8T+0ca7yFPz3U+         VrlA== |
| ARC-Authentication-Results | i=1; mx.google.com;       dkim=pass header.i=@accounts.google.com header.s=20161025 header.b=PJDwqydl;       spf=pass (google.com: domain of 3jf6oyagtapukl-obmivxzzlrkqp.dlldib.zlj@gaia.bounces.google.com designates 209.85.220.73 as permitted sender) smtp.mailfrom=3jF6oYAgTAPUkl-obmivXZZlrkqp.dlldib.Zlj@gaia.bounces.google.com;       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=accounts.google.com |
| Return-Path | <3jF6oYAgTAPUkl-obmivXZZlrkqp.dlldib.Zlj@gaia.bounces.google.com> |
| Received | from mail-sor-f73.google.com (mail-sor-f73.google.com. [209.85.220.73])        by mx.google.com with SMTPS id h10sor11348467qtp.54.2021.05.21.18.29.48        for <amrulloev.subhon@gmail.com>        (Google Transport Security);        Fri, 21 May 2021 18:29:48 -0700 (PDT) |
| Received-SPF | pass (google.com: domain of 3jf6oyagtapukl-obmivxzzlrkqp.dlldib.zlj@gaia.bounces.google.com designates 209.85.220.73 as permitted sender) client-ip=209.85.220.73; |
| Authentication-Results | mx.google.com;       dkim=pass header.i=@accounts.google.com header.s=20161025 header.b=PJDwqydl;       spf=pass (google.com: domain of 3jf6oyagtapukl-obmivxzzlrkqp.dlldib.zlj@gaia.bounces.google.com designates 209.85.220.73 as permitted sender) smtp.mailfrom=3jF6oYAgTAPUkl-obmivXZZlrkqp.dlldib.Zlj@gaia.bounces.google.com;       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=accounts.google.com |
| DKIM-Signature | v=1; a=rsa-sha256; c=relaxed/relaxed;        d=accounts.google.com; s=20161025;        h=mime-version:date:feedback-id:message-id:subject:from:to;        bh=4J4MOmQFvdqoF4iFFRFRsqKqHvOKXhnARkiTad9G+EA=;        b=PJDwqydlC5N1xeTr3Nq7OslqTpWCqSh7o2oK3zy32Vb0X/7RU0JfbVWeuPFzvRp9IC         10cQmRBfPdVdTsBtDl2BhQpNLn3z9RkBfKeGFpnQO1VmVIPqcaLnQpP1hajHySva+OK1         u0HV46C29DPjs667FEO9Pi9yYIopvP9MOmxIbSeScSCLiH3hwwUKsyXbu3IxSxcex71D         P66iBDRmxrwYmo/aXnobhCSpQ01WqtiI/vsJUIEpn9NVG9q6LnD7tPodlQ8Dz5U70HSH         BEn0PVx2IpCqullSQ/H7Zd3PQ6SfT9TpQP8G7AI6SCDCKXbc6m4opFvoDlwUFQvZTi51         UNeQ== |
| X-Google-DKIM-Signature | v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20161025;        h=x-gm-message-state:mime-version:date:feedback-id:message-id:subject         :from:to;        bh=4J4MOmQFvdqoF4iFFRFRsqKqHvOKXhnARkiTad9G+EA=;        b=LebPqCUDPH8jB4FV+zxlfcS/FYWUQ7Fds42oU5Xq5NWelMLY51NDbphftVS8zOqr3w         8f42Ypt1BWq3eK5eOmcoL3JYz8T1v//ojOBR2CWDGpBW0Gryhhl5XPnYrZ/DE3io0n3a         n9fBx8NEza/M3N1tVM25xjUZ23gIcldZ5r7ywbP5GmS1fc5JQo7E1IaG/YAGaUUyYGoG         6zbGYh5E93P50CSIFnq+WT3HnlGYktv/5yMPXAEM45hdRTGIl5878Ab7eRv8iYtkJ9EV         LZW9WmuUC4zZqL3fMKdRO0QDJCUizJak5AbY8j5fZOm+hcbbIP2V00UsL/xRVkJZJAUJ         fnJg== |
| X-Gm-Message-State | AOAM530bOc4QPbhSciTPEf/juZpgEl6ldxEimqgFh5lrYyYZ/bEdoKCN KdV7zk9snIr75zblQAi1/Z48avba0K5UcVHxPcyNWQ== |
| X-Google-Smtp-Source | ABdhPJyfGp1IkVl+/u0NbLLc8XjGHoaJbl9Li6VXcqVIrCVn8Qi2EySbnK9jE55+GVAdv3xvwO4DcXPDt8OLGNOve1D7Tg== |
| MIME-Version | 1.0 |
| X-Received | by 2002:ac8:5bc1:: with SMTP id b1mr13608184qtb.161.1621646988129; Fri, 21 May 2021 18:29:48 -0700 (PDT) |
| Date | Sat, 22 May 2021 01:29:47 GMT |
| X-Account-Notification-Type | 127-anexp#nret-fa |
| Feedback-ID | 127-anexp#nret-fa:account-notifier |
| X-Notifications | 1c9ca862cda00000 |
| Message-ID | <1hfrwKeuMkfuR6L7yQhUPg@notifications.google.com> |
| Subject | Security alert |
| From | Google <no-reply@accounts.google.com> |
| To | amrulloev.subhon@gmail.com |
| Content-Type | multipart/alternative; boundary="000000000000adb51305c2e11c0b" |
