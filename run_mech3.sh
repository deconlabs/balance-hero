for q in `seq 90 10 140`
do
    for p in `seq 0.8 0.1 1.2`
    do
        python3 run.py --n_episode=1000 --mechanism=3 --q_eps_decay=0.99 --p_eps_decay=0.99 --commission_pool=200 --price=$p --quantity=$q --http_port=3003 --cp_rate=-0.02
    done
done
