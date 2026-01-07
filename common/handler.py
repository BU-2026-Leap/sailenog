def lambda_handler(event, context):
    if not BUCKET:
        raise RuntimeError("BUCKET_NAME environment variable not set")

    ensure_csv_exists()

    obj = s3.get_object(Bucket=BUCKET, Key=KEY)
    text = obj["Body"].read().decode("utf-8")

    headline = get_top_headline()
    timestamp = datetime.utcnow().isoformat()

    text += f"\"{timestamp}\",\"{headline}\"\n"

    s3.put_object(
        Bucket=BUCKET,
        Key=KEY,
        Body=text.encode("utf-8"),
        ContentType="text/csv",
    )

    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Latest CNN Headline</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 40px;
          }}
          .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            max-width: 600px;
          }}
          h1 {{
            font-size: 22px;
          }}
          p {{
            color: #666;
          }}
        </style>
      </head>
      <body>
        <div class="card">
          <h1>{headline}</h1>
          <p>Fetched at {timestamp} UTC</p>
        </div>
      </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html
    }
