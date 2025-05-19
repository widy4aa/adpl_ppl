<div wire:poll.2000ms>
    <h2 class="text-xl font-bold mb-4">Monitoring Sensor</h2>

    @if(isset($Sensor['error']))
        <div class="text-red-500">Error: {{ $Sensor['error'] }}</div>
    @elseif($Sensor)
        <div class="grid grid-cols-2 gap-4">
            <p>Device ID: {{ $Sensor['data']['device_id'] }}</p>
            <p>Suhu udara: {{$Sensor['data']['suhu_udara']}}</p>
            <p>Suhu Tanah: {{$Sensor['data']['suhu_tanah']}}</p>
            <p>Kelembapan Udara: {{ $Sensor['data']['kelembapan_udara'] }}</p>
            <p>Kelembapan Tanah: {{ $Sensor['data']['kelembapan_tanah'] }}</p>
            <p>Last Update: {{ $Sensor['data']['last_update'] }}</p>
        </div>
    @else
        <div>Loading...</div>
    @endif

    <h2 class="text-xl font-bold mb-4 mt-6">Device Status</h2>

    @if(isset($Device['error']))
        <div class="text-red-500">Error: {{ $Device['error'] }}</div>
    @elseif($Device)
        <div class="grid grid-cols-2 gap-4">
            <div>
                <p>Controls Mode: {{ $Device['data']['mode'] }}</p>
                <button wire:click="toggleMode" class="px-2 py-1 bg-blue-500 text-white rounded">
                    {{ $Device['data']['mode'] === 'auto' ? 'Set Manual' : 'Set Auto' }}
                </button>
            </div>

            <div>
                <p>Lampu: {{ $Device['data']['lamp'] }}</p>
                <button wire:click="toggleLamp" class="px-2 py-1 bg-yellow-500 text-white rounded">
                    Toggle Lampu
                </button>
            </div>

            <div>
                <p>Pompa: {{ $Device['data']['water'] }}</p>
                <button wire:click="toggleWater" class="px-2 py-1 bg-green-500 text-white rounded">
                    Toggle Pompa
                </button>
            </div>

            <div>
                <p>Fan: {{ $Device['data']['fan'] }}</p>
                <button wire:click="toggleFan" class="px-2 py-1 bg-purple-500 text-white rounded">
                    Toggle Fan
                </button>
            </div>

            <p class="col-span-2">Last Update: {{ $Sensor['data']['last_update'] }}</p>
        </div>
    @else
        <div>Loading...</div>
    @endif

    <form action="/logout" method="POST" class="mt-6">
        @csrf
        <button class="bg-red-500 text-white px-4 py-2 rounded">Logout</button>
    </form>
</div>
