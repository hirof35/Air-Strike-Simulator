import math

class AirStrikeSimulator:
    def __init__(self, size=10):
        self.size = size
        # 10x10のグリッドマップを作成 (0: 空地, 1: ターゲット)
        self.map = [[0 for _ in range(size)] for _ in range(size)]
        self.targets = []

    def spawn_target(self, x, y, name="重要施設"):
        """マップ上にターゲットを配置"""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.map[y][x] = 1
            self.targets.append({"name": name, "x": x, "y": y, "hit": False})

    def display_map(self, strike_x=None, strike_y=None, radius=0):
        """現在のマップ状況を表示"""
        print("\n--- 現在のマップ状況 ---")
        for y in range(self.size):
            row_str = ""
            for x in range(self.size):
                # 爆撃範囲のプレビュー
                if strike_x is not None and math.hypot(x - strike_x, y - strike_y) <= radius:
                    if self.map[y][x] == 1:
                        row_str += "💥 "  # 被弾したターゲット
                    else:
                        row_str += "🔥 "  # 爆風範囲
                elif self.map[y][x] == 1:
                    row_str += "🎯 "  # 健全なターゲット
                else:
                    row_str += "🌲 "  # 通常の地形
            print(row_str)
        print("--------------------")

    def execute_strike(self, strike_x, strike_y, radius):
        """指定した座標を中心に、半径内のターゲットを破壊"""
        print(f"\n🚀 座標 ({strike_x}, {strike_y}) へ半径 {radius} の空爆を開始します...")
        
        destroyed_count = 0
        for target in self.targets:
            # 2点間の直線距離を計算 (ユークリッド距離)
            distance = math.hypot(target["x"] - strike_x, target["y"] - strike_y)
            
            if distance <= radius:
                target["hit"] = True
                print(f"💥 ヒット: {target['name']} (座標: {target['x']}, {target['y']}) が破壊されました！")
                destroyed_count += 1
                # マップ上の表示を更新
                self.map[target["y"]][target["x"]] = 0 
        
        if destroyed_count == 0:
            print("💨 効果なし：ターゲットに命中しませんでした。")
        else:
            print(f"✨ 戦果：合計 {destroyed_count} 個のターゲットを破壊。")

# === シミュレーションの実行 ===
if __name__ == "__main__":
    # 10x10のマップでシミュレーターを初期化
    sim = AirStrikeSimulator(size=10)
    
    # ターゲットを複数配置
    sim.spawn_target(3, 3, "敵司令部")
    sim.spawn_target(4, 3, "弾薬庫")
    sim.spawn_target(7, 8, "レーダー基地")
    
    # 空爆前のマップ表示
    print("【空爆前】")
    sim.display_map()
    
    # 1回目の空爆（座標 3, 3 に半径 1.5 で攻撃。隣接する弾薬庫も巻き込む）
    sim.execute_strike(strike_x=3, strike_y=3, radius=1.5)
    sim.display_map(strike_x=3, strike_y=3, radius=1.5)
    
    # 2回目の空爆（座標 7, 7 に半径 1.0 で攻撃。レーダー基地に届くか？）
    sim.execute_strike(strike_x=7, strike_y=7, radius=1.0)
    sim.display_map(strike_x=7, strike_y=7, radius=1.0)
