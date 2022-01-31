from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import BLACK_WON, COMPLETED, DRAW, WHITE_WON, Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_id = int(self.game_id)
        
        # Get necessary data for joining
        join_data = await self.get_join_data()

        await self.accept()
        await self.join_room(join_data)
        
    async def receive_json(self, content, **kwargs):
        print(f"{self.game_id} received json: ", content)
        command = content['gameCommand']
        
        if command == 'newMove':
            await self.send_new_move(content)
        elif command == 'gameOver':
            await self.game_over(content['winner'])

    async def join_room(self, join_data):
        pgn = join_data[0]
        white = join_data[1]

        # Determine side
        side = 'white'
        if not white:
            side = 'black'

        # Add consumer to the game's channel layer
        await self.channel_layer.group_add(
            str(self.game_id),
            self.channel_name
        )

        # Send join command to websocket
        await self.send_json({
            'gameCommand': 'join',
            'side': side,
            'pgn': pgn
            })

    async def send_new_move(self, event):
        # Send new move to everyone connected to the game
        await self.channel_layer.group_send(
            str(self.game_id), {
            'type': 'receive_new_move',
            'origin': event['origin'],
            'destination': event['destination'],
            'fen': event['fen'],
            'pgn': event['pgn'],
            'sender_channel': self.channel_name
        })

    async def receive_new_move(self, event):
        if self.channel_name != event['sender_channel']:
            await self.send_json({
                'gameCommand': 'newMove',
                'origin': event['origin'],
                'destination': event['destination'],
                'fen': event['fen'],
                'pgn': event['pgn']
            })
        await self.update_game(event['fen'], event['pgn'])

    @database_sync_to_async
    def game_over(self, winner):
        game = Game.objects.get(pk=self.game_id)

        # Determine if host won
        if winner == 'white':
            game.result = WHITE_WON

            if game.host_white == True:
                game.winner = game.host
            else:
                game.winner = game.opponent
        elif winner == 'black':
            game.result = BLACK_WON
            
            if game.host_white == True:
                game.winner = game.opponent
            else:
                game.winner = game.host
        elif winner == None:
            game.result = DRAW

        game.status = COMPLETED
        game.save()
    
    @database_sync_to_async
    def update_game(self, fen, pgn):
        game = Game.objects.get(pk=self.game_id)

        game.fen = fen
        game.pgn = pgn
        game.save()

    @database_sync_to_async
    def get_join_data(self):
        game = Game.objects.get(pk=self.game_id)
        pgn = game.pgn

        user = self.scope['user']
        white = None
        
        # Determine user side
        if game.host == user:
            white = game.host_white
        else:
            white = not game.host_white

        return [pgn, white]
