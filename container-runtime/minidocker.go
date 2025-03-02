package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"syscall"
)

const ImageBaseDir = "./imagesource"

func main() {
	if len(os.Args) < 2 {
		printHelp()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "pull":
		if len(os.Args) != 3 {
			fmt.Println("Usage: minidocker pull <image-name>")
			os.Exit(1)
		}
		pullImage(os.Args[2])

	case "run":
		if len(os.Args) < 4 {
			fmt.Println("Usage: minidocker run <image-name> <command> [args...]")
			os.Exit(1)
		}
		runContainer(os.Args[2], os.Args[3:])

	default:
		printHelp()
		os.Exit(1)
	}
}

func printHelp() {
	fmt.Println(`MiniDocker - A simple container runtime
Commands:
  pull <image-name>   Download and prepare a Docker image
  run <image-name> <command>  Run a command in the container
Example:
  minidocker pull nginx
  minidocker run nginx /usr/sbin/nginx`)
}

func pullImage(imageName string) {
	// Create image directory
	imageDir := filepath.Join(ImageBaseDir, imageName+"-root")
	if err := os.MkdirAll(imageDir, 0755); err != nil {
		fmt.Printf("Error creating image directory: %v\n", err)
		os.Exit(1)
	}

	// Docker commands
	fmt.Printf("Pulling image %s...\n", imageName)
	runCommand("docker", "pull", imageName)

	fmt.Printf("Creating temporary container...\n")
	containerID := runCommand("docker", "create", imageName)

	fmt.Printf("Exporting filesystem to %s...\n", imageDir)
	runCommand("docker", "export", containerID, "-o", filepath.Join(imageDir, "image.tar"))
	runCommand("tar", "-xf", filepath.Join(imageDir, "image.tar"), "-C", imageDir)

	// Cleanup
	os.Remove(filepath.Join(imageDir, "image.tar"))
	runCommand("docker", "stop", containerID)
	runCommand("docker", "rm", containerID)

	fmt.Printf("Successfully pulled %s to %s\n", imageName, imageDir)
}

func runContainer(imageName string, command []string) {
	imageDir := filepath.Join(ImageBaseDir, imageName+"-root")
	if _, err := os.Stat(imageDir); os.IsNotExist(err) {
		fmt.Printf("Image %s not found. Pull it first.\n", imageName)
		os.Exit(1)
	}

	// Create temporary runtime directory
	tempDir, err := os.MkdirTemp("", "minidocker-")
	if err != nil {
		fmt.Printf("Error creating temp directory: %v\n", err)
		os.Exit(1)
	}
	defer os.RemoveAll(tempDir)

	// Copy image files
	fmt.Printf("Preparing container filesystem...\n")
	runCommand("cp", "-a", imageDir+"/.", tempDir)

	// Create essential device files
	devDir := filepath.Join(tempDir, "dev")
	if err := os.MkdirAll(devDir, 0755); err != nil {
		fmt.Printf("Error creating dev directory: %v\n", err)
		os.Exit(1)
	}
	runCommand("sudo", "mknod", "-m", "666", filepath.Join(devDir, "null"), "c", "1", "3")

	// Run command in chroot
	fmt.Printf("Starting container...\n")
	cmd := exec.Command(command[0], command[1:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	syscall.Chroot(tempDir)
	cmd.Run()
}

func runCommand(name string, arg ...string) string {
	cmd := exec.Command(name, arg...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error running command: %s %v\n", name, arg)
		fmt.Printf("%s\n", output)
		os.Exit(1)
	}
	return string(output)
}