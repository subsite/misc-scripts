#!/bin/sh

####
#
# Script to enable ssh port forwarding on cPouta projects.
# Run after build on a machine with a Floating IP.
# Fredrik Welander 2021
#
# iptables -t nat -L # list nat rules
#
####

# Run as root
sudo -s

# Install iptables-persistent
apt update -y && apt install iptables-persistent nmap -y

# Enable ip forwarding
sysctl net.ipv4.ip_forward=1
# Make persistent
sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

# Flush all old NAT rules if any 
iptables -t nat -F

# Add port forwarding for ssh, connect to lan hosts on e.g. port 2210 to reach 192.168.1.10
iptables -t nat -A PREROUTING -p tcp --dport 2210 -j DNAT --to-destination 192.168.1.10:22
iptables -t nat -A PREROUTING -p tcp --dport 2211 -j DNAT --to-destination 192.168.1.11:22
iptables -t nat -A PREROUTING -p tcp --dport 2212 -j DNAT --to-destination 192.168.1.12:22
iptables -t nat -A PREROUTING -p tcp --dport 2213 -j DNAT --to-destination 192.168.1.13:22
iptables -t nat -A PREROUTING -p tcp --dport 2214 -j DNAT --to-destination 192.168.1.14:22
iptables -t nat -A PREROUTING -p tcp --dport 2215 -j DNAT --to-destination 192.168.1.15:22
iptables -t nat -A PREROUTING -p tcp --dport 2216 -j DNAT --to-destination 192.168.1.16:22
iptables -t nat -A PREROUTING -p tcp --dport 2217 -j DNAT --to-destination 192.168.1.17:22
iptables -t nat -A PREROUTING -p tcp --dport 2218 -j DNAT --to-destination 192.168.1.18:22
iptables -t nat -A PREROUTING -p tcp --dport 2219 -j DNAT --to-destination 192.168.1.19:22
iptables -t nat -A PREROUTING -p tcp --dport 2220 -j DNAT --to-destination 192.168.1.20:22
iptables -t nat -A PREROUTING -p tcp --dport 2221 -j DNAT --to-destination 192.168.1.21:22
iptables -t nat -A PREROUTING -p tcp --dport 2222 -j DNAT --to-destination 192.168.1.22:22
iptables -t nat -A PREROUTING -p tcp --dport 2223 -j DNAT --to-destination 192.168.1.23:22
iptables -t nat -A PREROUTING -p tcp --dport 2224 -j DNAT --to-destination 192.168.1.24:22
iptables -t nat -A PREROUTING -p tcp --dport 2225 -j DNAT --to-destination 192.168.1.25:22
iptables -t nat -A PREROUTING -p tcp --dport 2226 -j DNAT --to-destination 192.168.1.26:22
iptables -t nat -A PREROUTING -p tcp --dport 2227 -j DNAT --to-destination 192.168.1.27:22
iptables -t nat -A PREROUTING -p tcp --dport 2228 -j DNAT --to-destination 192.168.1.28:22
iptables -t nat -A PREROUTING -p tcp --dport 2229 -j DNAT --to-destination 192.168.1.29:22
iptables -t nat -A PREROUTING -p tcp --dport 2230 -j DNAT --to-destination 192.168.1.30:22
iptables -t nat -A PREROUTING -p tcp --dport 2231 -j DNAT --to-destination 192.168.1.31:22
iptables -t nat -A PREROUTING -p tcp --dport 2232 -j DNAT --to-destination 192.168.1.32:22
iptables -t nat -A PREROUTING -p tcp --dport 2233 -j DNAT --to-destination 192.168.1.33:22
iptables -t nat -A PREROUTING -p tcp --dport 2234 -j DNAT --to-destination 192.168.1.34:22
iptables -t nat -A PREROUTING -p tcp --dport 2235 -j DNAT --to-destination 192.168.1.35:22
iptables -t nat -A PREROUTING -p tcp --dport 2236 -j DNAT --to-destination 192.168.1.36:22
iptables -t nat -A PREROUTING -p tcp --dport 2237 -j DNAT --to-destination 192.168.1.37:22
iptables -t nat -A PREROUTING -p tcp --dport 2238 -j DNAT --to-destination 192.168.1.38:22
iptables -t nat -A PREROUTING -p tcp --dport 2239 -j DNAT --to-destination 192.168.1.39:22
iptables -t nat -A PREROUTING -p tcp --dport 2240 -j DNAT --to-destination 192.168.1.40:22
iptables -t nat -A PREROUTING -p tcp --dport 2241 -j DNAT --to-destination 192.168.1.41:22
iptables -t nat -A PREROUTING -p tcp --dport 2242 -j DNAT --to-destination 192.168.1.42:22
iptables -t nat -A PREROUTING -p tcp --dport 2243 -j DNAT --to-destination 192.168.1.43:22
iptables -t nat -A PREROUTING -p tcp --dport 2244 -j DNAT --to-destination 192.168.1.44:22
iptables -t nat -A PREROUTING -p tcp --dport 2245 -j DNAT --to-destination 192.168.1.45:22
iptables -t nat -A PREROUTING -p tcp --dport 2246 -j DNAT --to-destination 192.168.1.46:22
iptables -t nat -A PREROUTING -p tcp --dport 2247 -j DNAT --to-destination 192.168.1.47:22
iptables -t nat -A PREROUTING -p tcp --dport 2248 -j DNAT --to-destination 192.168.1.48:22
iptables -t nat -A PREROUTING -p tcp --dport 2249 -j DNAT --to-destination 192.168.1.49:22
iptables -t nat -A PREROUTING -p tcp --dport 2250 -j DNAT --to-destination 192.168.1.50:22
iptables -t nat -A PREROUTING -p tcp --dport 2251 -j DNAT --to-destination 192.168.1.51:22
iptables -t nat -A PREROUTING -p tcp --dport 2252 -j DNAT --to-destination 192.168.1.52:22
iptables -t nat -A PREROUTING -p tcp --dport 2253 -j DNAT --to-destination 192.168.1.53:22
iptables -t nat -A PREROUTING -p tcp --dport 2254 -j DNAT --to-destination 192.168.1.54:22
iptables -t nat -A PREROUTING -p tcp --dport 2255 -j DNAT --to-destination 192.168.1.55:22
iptables -t nat -A PREROUTING -p tcp --dport 2256 -j DNAT --to-destination 192.168.1.56:22
iptables -t nat -A PREROUTING -p tcp --dport 2257 -j DNAT --to-destination 192.168.1.57:22
iptables -t nat -A PREROUTING -p tcp --dport 2258 -j DNAT --to-destination 192.168.1.58:22
iptables -t nat -A PREROUTING -p tcp --dport 2259 -j DNAT --to-destination 192.168.1.59:22
iptables -t nat -A PREROUTING -p tcp --dport 2260 -j DNAT --to-destination 192.168.1.60:22
iptables -t nat -A PREROUTING -p tcp --dport 2261 -j DNAT --to-destination 192.168.1.61:22
iptables -t nat -A PREROUTING -p tcp --dport 2262 -j DNAT --to-destination 192.168.1.62:22
iptables -t nat -A PREROUTING -p tcp --dport 2263 -j DNAT --to-destination 192.168.1.63:22
iptables -t nat -A PREROUTING -p tcp --dport 2264 -j DNAT --to-destination 192.168.1.64:22
iptables -t nat -A PREROUTING -p tcp --dport 2265 -j DNAT --to-destination 192.168.1.65:22
iptables -t nat -A PREROUTING -p tcp --dport 2266 -j DNAT --to-destination 192.168.1.66:22
iptables -t nat -A PREROUTING -p tcp --dport 2267 -j DNAT --to-destination 192.168.1.67:22
iptables -t nat -A PREROUTING -p tcp --dport 2268 -j DNAT --to-destination 192.168.1.68:22
iptables -t nat -A PREROUTING -p tcp --dport 2269 -j DNAT --to-destination 192.168.1.69:22
iptables -t nat -A PREROUTING -p tcp --dport 2270 -j DNAT --to-destination 192.168.1.70:22
iptables -t nat -A PREROUTING -p tcp --dport 2271 -j DNAT --to-destination 192.168.1.71:22
iptables -t nat -A PREROUTING -p tcp --dport 2272 -j DNAT --to-destination 192.168.1.72:22
iptables -t nat -A PREROUTING -p tcp --dport 2273 -j DNAT --to-destination 192.168.1.73:22
iptables -t nat -A PREROUTING -p tcp --dport 2274 -j DNAT --to-destination 192.168.1.74:22
iptables -t nat -A PREROUTING -p tcp --dport 2275 -j DNAT --to-destination 192.168.1.75:22
iptables -t nat -A PREROUTING -p tcp --dport 2276 -j DNAT --to-destination 192.168.1.76:22
iptables -t nat -A PREROUTING -p tcp --dport 2277 -j DNAT --to-destination 192.168.1.77:22
iptables -t nat -A PREROUTING -p tcp --dport 2278 -j DNAT --to-destination 192.168.1.78:22
iptables -t nat -A PREROUTING -p tcp --dport 2279 -j DNAT --to-destination 192.168.1.79:22
iptables -t nat -A PREROUTING -p tcp --dport 2280 -j DNAT --to-destination 192.168.1.80:22
iptables -t nat -A PREROUTING -p tcp --dport 2281 -j DNAT --to-destination 192.168.1.81:22
iptables -t nat -A PREROUTING -p tcp --dport 2282 -j DNAT --to-destination 192.168.1.82:22
iptables -t nat -A PREROUTING -p tcp --dport 2283 -j DNAT --to-destination 192.168.1.83:22
iptables -t nat -A PREROUTING -p tcp --dport 2284 -j DNAT --to-destination 192.168.1.84:22
iptables -t nat -A PREROUTING -p tcp --dport 2285 -j DNAT --to-destination 192.168.1.85:22
iptables -t nat -A PREROUTING -p tcp --dport 2286 -j DNAT --to-destination 192.168.1.86:22
iptables -t nat -A PREROUTING -p tcp --dport 2287 -j DNAT --to-destination 192.168.1.87:22
iptables -t nat -A PREROUTING -p tcp --dport 2288 -j DNAT --to-destination 192.168.1.88:22
iptables -t nat -A PREROUTING -p tcp --dport 2289 -j DNAT --to-destination 192.168.1.89:22
iptables -t nat -A PREROUTING -p tcp --dport 2290 -j DNAT --to-destination 192.168.1.90:22
iptables -t nat -A PREROUTING -p tcp --dport 2291 -j DNAT --to-destination 192.168.1.91:22
iptables -t nat -A PREROUTING -p tcp --dport 2292 -j DNAT --to-destination 192.168.1.92:22
iptables -t nat -A PREROUTING -p tcp --dport 2293 -j DNAT --to-destination 192.168.1.93:22
iptables -t nat -A PREROUTING -p tcp --dport 2294 -j DNAT --to-destination 192.168.1.94:22
iptables -t nat -A PREROUTING -p tcp --dport 2295 -j DNAT --to-destination 192.168.1.95:22
iptables -t nat -A PREROUTING -p tcp --dport 2296 -j DNAT --to-destination 192.168.1.96:22
iptables -t nat -A PREROUTING -p tcp --dport 2297 -j DNAT --to-destination 192.168.1.97:22
iptables -t nat -A PREROUTING -p tcp --dport 2298 -j DNAT --to-destination 192.168.1.98:22
iptables -t nat -A PREROUTING -p tcp --dport 2299 -j DNAT --to-destination 192.168.1.99:22

# Masquerade, note exclude loopback, otherwis nslookup will stop working
iptables ! -o lo -t nat -A POSTROUTING -j MASQUERADE 

# Make iptables rules persistent
iptables-save > /etc/iptables/rules.v4

