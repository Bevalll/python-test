# 另一个文件中的使用示例（如 test_module.py）
import AreaVolume

# 使用模块中的函数
r = 5
area = AreaVolume.circle_area(r)
volume = AreaVolume.sphere_volume(r)

print(f"半径为{r}的圆面积：{area:.2f}")
print(f"半径为{r}的球体积：{volume:.2f}")