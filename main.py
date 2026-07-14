import os
import sys

def gen_docker_compose(start_port: int = 1080, end_port: int = 1087):
  all_str = "services:\n"
  for i in range(start_port, end_port):
    all_str += f"""  warp_{i}:
    build: .
    image: warp_daisuki:latest
    container_name: warp_{i}
    sysctls:
      - net.ipv6.conf.all.disable_ipv6=0
    ports:
      - "{i}:1080/tcp"
      - "{i}:1080/udp"
    environment:
      - LANG=C.UTF-8
    networks:
      - warp_net
    restart: unless-stopped

"""
  all_str += """networks:
  warp_net:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"
    enable_ipv6: true
    ipam:
      config:
        - subnet: 172.20.0.0/24
        - subnet: "fd00:dead:beef::/48"
"""
  return all_str

def gen_clash_config(start_port: int = 1080, end_port: int = 1087):
  with open("templates/config.yaml") as f:
    lines = f.readlines()
  proxy_names = []
  proxy_texts = []
  
  for port in range(start_port, end_port):
    name = f"Warp-{port}"
    proxy_names.append(name)
    proxy_texts.append(f"  - name: \"{name}\"")
    proxy_texts.append(f"    type: socks5")
    proxy_texts.append(f"    server: 127.0.0.1")
    proxy_texts.append(f"    port: {port}")

  group_texts = []
  group_texts.append(f"  - name: \"PROXY\"")
  group_texts.append(f"    type: load-balance")
  group_texts.append(f"    strategy: round-robin")
  group_texts.append(f"    url: \"http://www.gstatic.com/generate_204\"")
  group_texts.append(f"    interval: 300")
  group_texts.append(f"    proxies:")
  for name in proxy_names:
    group_texts.append(f"      - \"{name}\"")

  new_lines = []
  for line in lines:
    new_lines.append(line)
    if line.strip() == "proxies:":
      new_lines.extend([t + "\n" for t in proxy_texts])
    elif line.strip() == "proxy-groups:":
      new_lines.extend([t + "\n" for t in group_texts])

  return "".join(new_lines)

def main(argc: int, argv: list[str]) -> int:
  # check if the output directory exists, if not, create it
  if not os.path.exists("output"):
    os.makedirs("output")
  if argc < 2:
    print("Usage: python main.py <number_of_warp_instances>")
    return 1
  docker_compose_content = gen_docker_compose(1080, 1080 + int(argv[1]))
  with open("output/docker-compose.yml", "w") as f:
    print(f"docker-compose.yml:\n{docker_compose_content}\n")
    f.write(docker_compose_content)
  clash_config_content = gen_clash_config(1080, 1080 + int(argv[1]))
  with open("output/clash_config.yaml", "w") as f:
    print(f"clash_config.yaml:\n{clash_config_content}\n")
    f.write(clash_config_content)
  return 0

if __name__ == "__main__":
  sys.exit(main(len(sys.argv), sys.argv))