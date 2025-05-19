<?php

namespace App\Livewire;

use Illuminate\Support\Facades\Http;
use Livewire\Component;

class Monitoring extends Component
{
    public $Sensor;
    public $Device;

    public function mount()
    {
        $this->fetchApi();
    }

    public function fetchApi()
    {
        try {
            $response = Http::get('http://127.0.0.1:5000/api/sensor/info');

            if ($response->successful()) {
                $this->Sensor = $response->json();
                //dd($this->Sensor);
            } else {
                $this->Sensor = ['error' => 'Gagal ambil data'];
            }
        } catch (\Exception $e) {
            $this->Sensor = ['error' => $e->getMessage()];
        }

        try {
            $response = Http::get('http://127.0.0.1:5000/api/device/info');

            if ($response->successful()) {
                $this->Device = $response->json();
                //dd($this->Device);
            } else {
                $this->Device = ['error' => 'Gagal ambil data'];
            }
        } catch (\Exception $e) {
            $this->Device = ['error' => $e->getMessage()];
        }
    }
    public function render()
    {
        $this->fetchApi();
        return view('livewire.monitoring');
    }
}
