import pusher

pusher_client = pusher.Pusher(
  app_id='1883370',
  key='ddb32833a240a2caee60',
  secret='2c4d1f0de041ac400d56',
  cluster='ap2',
  ssl=True
)

# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})