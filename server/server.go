package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo"

	"github.com/archproj/slackoverflow/config"
	"github.com/archproj/slackoverflow/database"
	"github.com/archproj/slackoverflow/slack"
	"github.com/archproj/slackoverflow/routes"
)

const (
	VERSION = "0.1.0"
)

func main() {
	cfg, err := config.Load() // from environment
	if err != nil {
		log.Panic(err)
	}

	e := echo.New()

	// test db connection and create tables
	db, err := database.Init(cfg)
	if err != nil {
		log.Panic(err)
	}

        // create clients and find channel
	sc, err := slack.Init(cfg)
	if err != nil {
		log.Panic(err)
	}

	routes.Serve(cfg, e, db, sc)

	go func() {
		if err := e.Start(fmt.Sprintf("%s:%s", cfg.Host, cfg.Port)); err != nil {
			e.Logger.Info("shutting down the server.")
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server with
	// a timeout of 10 seconds.
	quit := make(chan os.Signal)
	signal.Notify(quit, os.Interrupt)

	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}
